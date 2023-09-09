---
title: "[Fluent Python] Ch8. Type Hints in Functions"
categories: [Dev, Python]
math: true
---

## Gradual Type System

* Is Optional
  * Be default, the type checker does not emit warnings for no type hints.
* Does not catch type errors in runtime
  * Type hints are only checked by static type checkers, linters, and IDEs to raise warning.
* Does not enhance performance


## Gradual Type Hint with Mypy

Mypy is a popular Python type checker. You can install Mypy with

```shell
pip install mypy
```

`messages.py`
```python
def show_count(count, word):
    if count == 1:
        return f"1 {word}"
    count_str = str(count) if count else 'no'
    return f"{count_str} {word}s"

print(show_count(99, "bird")) # 99 birds
print(show_count(1, "bird")) # 1 bird
print(show_count(0, "bird")) # no birds
```

Type check `messages.py` by

```shell
mypy messages.py
```

By default, mypy does not enforce type hints for functions.

### Make Mypy More Strict

* `--disallow-untyped-defs` option
    * In order to enforce type hints on all functions, use `--disallow-untyped-defs` option.
    ```shell
    mypy --disallow-untyped-defs messages.py
    ```
    ![Alt text](/assets/img/python/ch3-1.png)
* `--disallow-incomplete-defs`
    ```python
    def show_count(count, word) -> str:
        if count == 1:
            return f"1 {word}"
        count_str = str(count) if count else 'no'
        return f"{count_str} {word}s"
    ```
    * When provided type hint only for return, then this option will raise a flag.
    ![Alt text](/assets/img/python/ch8-2.png)
    * This way, you can gradually add type hints function by function without getting warnings about functions that you haven't annotated

Instead of providing command-line options, you can provide `mypy.ini` file for settings.

```text
python_version = 3.9
warn_unused_configs = True
disallow_incomplete_defs = True
```

## A Default Parameter Value

The `show_count` function in `messages.py` does not allow plural noun such as "children".

Let's add a test code.

`messages_test.py`
```python
def test_irregular() -> None:
    got = show_count(2, 'child', 'children')
    assert got == '2 children'
```

If we run `mypy messages_test.py`, Mypy detects the error

![Alt text](/assets/img/python/ch8-3.png)

> Don't forget to add the return type hint, otherwise Mypy will not check it
{: .prompt-warning}

## flake8 and blue for Code Style

A recommended code style for type hints are

1. No space b/w the parameter name and the `:`, one space after the `:`
2. Spaces on both sides of `=` that precedes a default param value

* Use tools like **flake8** and **blue** to make enforce standardized code style.

## Using None as Default

```python
def show_count(count: int, singular: str, plural: str = '') -> str:
    if count == 1:
        return f'1 {singular}'
    count_str = str(count) if count else 'no'
    if not plural:
        plural = singular + 's'
    return f'{count_str} {plural}'
```

The `plural` parameter has a default argument `''`. 

However, in other contexts, especially when the optional parameter is a **mutable type**. Then, `None` is the only sensible default.

To have `None` as the default parameter,

```python
from typing import Optional

def show_count(count: int, singular: str, plural: Optional[str] = None) -> str:
    ...
```

* `Optional[str]` means plural can be `str` or `None`

## Types Are Defined by Supported Operations

* It's more useful to consider the **set of supported operations** as the defining characteristic of a type


## Simple Types and Classes

* Simple types can be directly used in type hints
  * `int`
  * `float`
  * `str`
  * `bytes`
* Concrete classes from the **standard library**, **external packages**, or **user defined** can be used in type hints
  * ex) `def func(p: Person, d: Duck)`

Among classes, **consistent-with** is defined like **subtype-of**
* A subclass is **consistent-with** all its superclasses

> One exception: `int` is **consistent-with** `complex`
>
> "Practically beats purity" - There's no nominal subtype relationship b/w `int`, `float`, and `complex`. However, PEP 484 declares that `int` is consistent-with `float`, and `float` is consistent-with `complex`. It makes sense because `int` implements all operations of `float` and `int` implements additional ones such as `&, |, <<`, etc. For `i=3`, `i.real = 3`, `i.imag = 0`.
{: .prompt-warning}

## Optional and Union Types

* `Optional[str]` is a shortcut for `Union[str, None]`: means it could be `str` or `None`

> Better Syntax for Optional & Union in Python 3.10
>
> We can write `str | bytes` instead of `Union[str, bytes]` since Python 3.10.
> The `|` operator also works with `isinstance` and `issubclass`. (ex. `isinstance(x, int | str)`)
{: .prompt-info}

> Avoid functions that return `Union` types
>
> They put an extra burden on the user - forcing them to check the type of the returned value at **runtime** to know what to do with it!
{: .prompt-warning}

> Nested `Union` types have the same effect as a flattened `Union`.
>
> `Union[A, B, Union[C, D, E]]` is the same as `Union[A, B, C, D, E]`
{: .prompt-warning}

`Union` is more useful with types that are **not consistent among themselves**
* `Union[int, float]` is redundant since `int` is **consistent-with** `float`.
* We can just use `float` to annotate the parameter since it accepts `int` as well.

## Generic Collections

Generic types can be declared with type params to **specify the type of items they can handle**
```python
def tokenize(text: str) -> list[str]:
    reeturn text.upper().split()
```
* `list` can be parametrized to constrain the **type of elements** in it
* `tokenize` returns a `list` where every item is of type `str`
* **PEP 585** lists collections from the standard library accepting generic type hints. They only show collections that use the **simplest form** like `container[item]`
  * `list`
  * `set`
  * `frozenset`
  * `collections.deque`
  * `abc.Container`
  * `abc.Collection`
  * `abc.Sequence`
  * `abc.Set`
  * `abc.MutableSequence`
  * `abc.MutableSet`
* We'll see later types that support more complex type hints like `tuple` and `mapping`

> For Python 3.7 and 3.8, you need a `__future__` import to make `[]` notation work with built-in collections such as `list`.
> ```python
> from __future__ import annotations
> def tokenize(text: str) -> list[str]:
>   return text.upper().split()
> ```
> For Python 3.5 and 3.6, you must use `typing` module
> ```python
> from typing import List
> def tokenize(text: str) -> List[str]:
>     return text.upper().split()
> ```
{: .prompt-info}

## Tuple Types

There're 3 ways to annotate tuple types
1. Tuples as <span class="hl">records</span>
   * Use the `tuple` built-in and declare the types of the fields within `[]`
   * Ex) `tuple[str, float, str]` to accept a tuple with city name, population, and country: `('Seoul', 24.25, 'Korea')`
2. Tuples as <span class="hl">records with named fields</span>
   * To annotate a tuple with many fields, or specific types of tuple your code uses in different places, use **typing.NamedTuple**
  
   ```python
    from typing import NamedTuple
    PRECISION = 9

    class Coordinate(NamedTuple):
        lat: float
        lon: float
    
    def geohash(lat_lon: Coordinate) -> str:
        return gh.encode(*lat_lon, PRECISION)
   ```
   * `typeing.NamedTuple` is a factory for `tuple` subclasses, so `Coordinate` is **consistent-with** `tuple[float, float]` but the **reverse is not true** since `Coordinate` has extra methods added by `NamedTuple` like `._asdict()` or user-defined functions.
   * In practice, it's allowed to pass `Coordinate` instace to the following function
   
   ```python
   def display(lat_lon: tuple[float, float]) -> str:
     ...
   ```
3. Tuples as **immutable sequences**
   * To annotate tuples with **unspecified length** that are used as **immutable lists**, you must specify a **single type**, followed by `...`.
     * `tuple[int, ...]` is a tuple with `int` items
     * The ellipsis indicates that any number of elements >= 1 is acceptable
     * (There's no way to specify types for arbitrary length tuple of course)
     * So `def func(x: tuple[Any, ...])` is the same as `def fun(x: tuple)`

## Generic Mappings

* Generic mapping types are annotated as `MappingType[KeyType, ValueType]`.
* For Python >= 3.9, the built-in `dict` and the mapping types in `collections` and `collections.abc` accept that notation.
* For earlier versions, you must use `typing.Dict` and other mapping types from `tying` module.

## Abstract Base Classes

> "Be conservative in what you send, be liberal in what you accept" - Postel's law, a.k.a. the Robustness Principle

```python
from collections.abc import Mapping
def name2hex(name: str, color_map: Mapping[str, int]) -> str:
  ...
```

> Ideally, a function should accept arguments of **abstract types**
{: .prompt-info}

* Ideally, a function should accept arguments of **abstract types** (or `typing` equivalent), not concrete types to give more flexibility to the caller
* Using `abc.Mapping`, the caller can pass an instance of `dict`, `defaultdict`, `ChainMap`, `UserDict` subclass or any other type that is a **subtype-of** `Mapping`.

In contrast, let's see what happens if the argument accepts a concrete type.

```python
def name2hex(name: str, color_map: dict[str, int]) -> str:
  ...
```

* Now, `color_map` must be a `dict` or one of its subtypes such as `defaultdict` or `OrderedDict`.
* A subclass of `collections.UserDict` **would not pass** the type check such as Mypy since it's not a subclass of `dict`.
* `dict` and `collections.UserDict` are siblings - both are subclasses of `abc.MutableMapping`
* Hence, it's better to use `abc.Mapping` or `abc.MutableMapping` in type hints, instead of `dict`
* Moreover, if the `name2hex` does not mutate `color_map`, then the most accurate type hint is `abc.Mapping`
  * The caller doesn't need to provide an object that implements methods like `setdefault`, `pop`, `update` - they're part of `MutableMapping` interface , but not of `Mapping`
  * "Be liberal in what you accept"

> A function should return **concrete types**
{: .prompt-info}

```python
def tokenize(text: str) -> list[str]:
  return text.upper().split()
```

## Iterable

> The `typing.List` documentations recommends to use `Sequence` and `Iterable` for function parameter type hints
{: .prompt-info}

```python
from collections.abc import Iterable

FromTo = tuple[str, str]

def zip_replace(text: str, changes: Iterable[FromTo]) -> str:
  ...
```

```python
zip_replace(
  "abc",
  [('a', '4'), ('e', '5')]
)
```

* `FromTo` is a <span class="hl">type alias</span> fo `tuple[str, str]` (more readable)

> **Explicit TypeAlias in Python 3.10**
>
> PEP 613 introduced a special type `TypeAlias` to make the assignments that create type aliases more visible and easier to type check.
>
> ```python
> from typing import TypeAlias
> FromTo: TypeAlias - tuple[str, str]
> ```
{: .prompt-info}

> **Stub Files and the Typeshed Project**
>
> As of Python 3.10, the **standard library has no annotations**. But Mypy, PyCharm, etc can find the type hints in the **Typeshet** project, in the form of **stub files**, special source files with `.pyi` extension, that have annotated function and method signature just like header files in C.
{: .prompt-info}

### `abc.Iterable` vs `abc.Sequence`

```python
from collections.abc import Sequence

def func1(sequence: Sequence[str]) -> int:
  return len(sequence)
```

```python
from collections.abc import Iterable
def func2(lst: Iterable[int]) -> int:
  _sum = 0
  for e in lst:
    _sum += e
  return _sum
```

* `Iterable`
  * `func1` must iterate over the **entire Iterable** to return a result.
    * Given an **endless iterable** such as `itertools.cycle` would consume all memory
  * Despite this potential danger, it's common to offer functions that accept `Iterable` to allow the caller to provide the input data as **generator** to save a lot of memory
* `Sequence`
  * `func2` must accept `Sequence` because it must get the `len()` of the input.
