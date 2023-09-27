---
title: "[SQLAlchemy] Transactions and DBAPI"
categories: [Dev, SQLAlchemy]
math: true
---

Reference: [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html#tutorial-working-with-transactions)

## The Engine

Every SQLAlchemy application connecting to a database needs an `Engine` object which is a central source of connections to a database providing
1. A factory
2. Holding space called a **connection pool** for database connections

```python
from sqlalchemy import create_engine

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
```

* <span class="hl">Dialect</span>
  * A Python object that represents information and methods that allow DB operations to proceed on a particular database backend a particular python driver (or DBAPI).
  * `sqlite` portion
* <span class="hl">DBAPI</span>
  * A 3rd party driver that SQLAlchemy uses to interact with a particular database
  * `pysqlite` portion

> **Lazy Connecting**
>
> The `Engine` returned by `create_engine()` does not automatically connect to the database. The connection happens only the first time it performs a task against the database.
{: .prompt-info}


Let's look at basic operations of `Engine` and its primary interactive endpoints `Connection` and `Result`.

> Relationship with ORM
>
> The `Engine` is managed by an object called `Session` in **ORM** world.
>
> The `Session` is largely identical to `Connection` discussed below.
{: .prompt-info}


## Getting a Connection

> `text()`
>
> We'll use `text()` that allows us to write **SQL statements** as textual SQL. However, we'll learn the **SQLAlchemy Expression Language** later as use of `text()` is rare in most cases.
{: .prompt-info}

The sole purpose of `Engine` is to provide a **unit of connectivity to the database** called `Connection`.

The `Connection` object is how all interaction with a database is done when working with the Core directly.

As the `Connection` represents an "open resource" against the database, we want to **limit the scope of our use of this object to a specific context**.
* The best way to do this is Python context manager `with`.

```python
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

with engine.connect() as conn:
    print(type(conn)) # <class 'sqlalchemy.engine.base.Connection'>
    result = conn.execute(text("SELECT 'hello world'"))
    print(type(result)) # <class 'sqlalchemy.engine.cursor.CursorResult'>
    print(result.all()) # [('hello world',)]
```
* Textual SQL is emitted with `text()`
* `conn` is the `Connection` instance.
* The context manager framed the operation inside of a **transaction**.
  * The default behavior of the Python DBAPI includes that a **transaction is always in progress**
* When the connection is released, a **ROLLBACK** is emitted to end the transaction.
* The result of SELECT is an object called `Result`

With `create_engine(..., echo=True)`, we can see the full log of what's happening within the transaction.

```bash
(sqlalchemy-tutorial-py3.11) ~/Desktop/sqlalchemy-tutorial ᐅ python 1_engine.py
<class 'sqlalchemy.engine.base.Connection'>
2023-09-26 22:37:53,240 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2023-09-26 22:37:53,240 INFO sqlalchemy.engine.Engine SELECT 'hello world'
2023-09-26 22:37:53,240 INFO sqlalchemy.engine.Engine [generated in 0.00011s] ()
<class 'sqlalchemy.engine.cursor.CursorResult'>
[('hello world',)]
2023-09-26 22:37:53,241 INFO sqlalchemy.engine.Engine ROLLBACK
```

We can see that ROLLBACK is indeed triggered at the end to finish the transaction.

> The transaction is **NOT committed automatically!**
>
> To commit the data, we must call `Connection.commit()` explicitly.
{: .prompt-warning}

## Committing Changes

The DBAPI connection, by default, is **non-autocommitting**.

To commit changes, we can use `Connection.commit()` method **inside the context**.

### Commit As You Go Style

```python
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit() # commit changes to the database
```

* We emitted two SQl statements `CREATE TABLE` and `INSERT` which are in a transaction usually.
* We invoked `conn.commit()` to commit this transaction to the database.
* <span class="hl">Commit as you go</span>
  * After this call, we're free to make more changes and call `Connection.commit()`. SQLAlchemy refers to this style as commit as you go.

### Begin Once Style

Another way to commit changes is to use `Engine.begin()` to declare our "connect" block to be a **transaction block**.

This style is referred to as <span class="hl">begin once</span>.

```python
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
    
with engine.begin() as conn:
  conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
    )
```

> **DDL (Data Definition Language)**
>
> DDL is the subset of SQl that relational databases use to **configure tables, constraints, and other permanent objects** within a database schema.
>
> Ex) `CREATE TABLE` is one example of DDL, and is recommended to be within a **transaction block that ends with COMMIT**.
{: .prompt-tip}

## Fetching Rows

In the previous example, executing `SELECT` statement returns an object called `Result`.


```python
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('sqlite+pysqlite:///:memory:')
    
with engine.begin() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
    )
    
    result = conn.execute(text("SELECT x, y FROM some_table"))
    print(type(result))  # <class 'sqlalchemy.engine.cursor.CursorResult'>
```

* `Result` object is an **iterable** object of `Row` objects.
  ```python
  print(type(next(result)))  # <class 'sqlalchemy.engine.row.Row'>
  ```
* The `Row` object acts like Python **named tuple**.
  ```python
  row1 = next(result)
  print(row1.x, row1.y)  # 6 8
  ```
* `Result.all()` returns a `list[Row]`
  ```python
  result_all = result.all()
  print(type(result_all))  # <class 'list'>
  print(type(result_all[0]))  # <class 'sqlalchemy.engine.row.Row'>
  ```

### 1. Tuple Assignment

```python
result = conn.execute(text("SELECT x, y FROM some_table"))

for x, y in result:
  ...
```
### 2. Integer Index

```python
result = conn.execute(text("SELECT x, y FROM some_table"))

for row in result:
  x = row[0]
  ...
```

### 3. Attribute Name

Rows behave like Python named tuples so you can access with attribute names, matching the names of each column.

```python
result = conn.execute(text("SELECT x, y FROM some_table"))

for row in result:
  print(f"Row: {row.x} {row.y}")
```

### 4. Mapping Access

To receive rows as Python **mapping objects**, the `Result` can be transformed into a `MappingResult` object using `Result.mappings()`.

```python
result = conn.execute(text("SELECT x, y FROM some_table"))

for dict_row in result.mappings():
  x = dict_row['x']
  y = dict_row['y']
```

# Sending Parameters

As we saw in `INSERT` statement, SQL statements are usually accompanied by **data to be passed** with the statement.

`Connection.execute()` method accepts parameters, known as <span class="hl">bound parameters</span>.


```python
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('sqlite+pysqlite:///:memory:')
    
with engine.begin() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 9, "y": 10}]
    )
    
    result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 9})
    for row in result:
        print(f"x: {row.x} y: {row.y}")
```

* `text()` accepts a colon format `:y`. Then, the actual value for that is passed as the second argument to `Connection.execute()` in dictionary format.

> **Always Use Bound Parameters**
> 
> When using textual SQL, a Python literal value, even non-strings like integers or dates should **never be stringified into SQL string directly**.
>
> A **parameter should ALWAYS be used**.
{: .prompt-warning}

We can also insert **multiple rows** at once.

For [DML](https://docs.sqlalchemy.org/en/20/glossary.html#term-DML) statements such as `INSERT`, `UPDATE`, and `DELETE`, we can send **multiple parameter sets** to `Connection.execute()`.

We can pass a list of dictionaries instead of a single dictionary, which indicates that the **single SQL statement should be invoked multiple times**, once for each parameter set.
* This style of execution is known as <span class="hl">executemany</span>

```python
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('sqlite+pysqlite:///:memory:')
    
with engine.begin() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
    )
```

## Executing with an ORM Session

Most of the examples we learned are applicable to **ORM** as well.

> The `Session`
>
> The fundamental database-interactive object when using ORM is called the `Session`, very similar to `Connection`.
{: .prompt-info}

There're different ways to create `Session` but below is one simple way.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import text

engine = create_engine('sqlite+pysqlite:///:memory:')
    
with Session(engine) as session:
    session.execute(text("CREATE TABLE some_table (x int, y int)"))
    session.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
    )
    
    result = session.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 9})
    for row in result:
        print(f"x: {row.x} y: {row.y}")
    session.commit()
```

You can see that pretty much all things are similar to Connection.

> The `Session` does not hold onto the `Connection` object **after it ends the transaction**. It gets a **new** `Connection` from the `Engine`.
{: .prompt-info}

See more about `Session`: [Session Basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#id1)
