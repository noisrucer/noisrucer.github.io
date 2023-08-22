---
title: "[Fluent Python] Ch7. Functions as First-Class Objects"
categories: [Dev, Python]
math: true
---

## Table of Contents <!-- omit from toc -->
- [1. Treating a Function Like an Object](#1-treating-a-function-like-an-object)
- [2. Higher-Order Functions](#2-higher-order-functions)
- [3. List Comprehension: Modern Replacement for map, filter, and reduce](#3-list-comprehension-modern-replacement-for-map-filter-and-reduce)
- [4. Anonymous Functions](#4-anonymous-functions)
- [5. The Nine Flavors of Callable Objects](#5-the-nine-flavors-of-callable-objects)
- [6. User-Defined Callable Types](#6-user-defined-callable-types)
- [7. From Positional to Keyword-Only Paramaters](#7-from-positional-to-keyword-only-paramaters)
- [8. Positional-Only Parameters](#8-positional-only-parameters)
- [9. Packages for Functional Programming](#9-packages-for-functional-programming)
- [10. Freezing Arguments with `functools.partial`](#10-freezing-arguments-with-functoolspartial)

## 1. Treating a Function Like an Object

<span class="hl">First-class object</span>
* Created at runtime
* Assigned to a variable or element in a data structure
* Passed as an argument to a function
* Returned as the result of a function

```python
def factorial(n):
    "return n!"
    return 1 if n < 2 else n * factorial(n - 1)

print(factorial(42)) # 14050061177...
print(factorial.__doc__) # 'returns n!'
print(type(factorial) # <class 'function'>
```

* `__doc__` is one of several **attributes** of function objects
* `factorial` is an **instance** of the `function` class

```python
fact = factorial
print(fact) # <function factorial at 0x...>
print(fact(5)) # 120
print(map(factorial, range(11))) # <map object at 0x...>
print(list(map(factorial, range(11)))) # [1, 1, 2, 6, ..., 3628800]
```

* We can see that the "first class" nature of a function object
* We can **assign** the function object to a variable `fact` and call it
* We can pass the function object as an **argument** to the `map` function

## 2. Higher-Order Functions

* <span class="hl">Higher-order functions</span>: A function that takes a function as an argument or returns a function.
* ex) `sorted` - takes a function(one argument function) as an argument for `key` parameter.
    ```python
    names = ["Jason", "Jack", "Bob", "Alice"]
    >>> sorted(names, key=len) # ["Bob", "Jack", "Alice", "Jason]
    ```
* ex) `map` - Takes an function as the first argument to be applied to each of element in the second iterable.

## 3. List Comprehension: Modern Replacement for map, filter, and reduce

* `map` and `filter` functions are built-ins in Python 3 but <span class="hl">list comprehension</span> and <span class="hl">generator expressions</span> replace them elegantly.
  * Things you can do with `map` and `filter`, you can do better with **listcomp** and **genexp**.
  * Listcomps and genexps are more readable than map and filter.
  * In Python 3, `map` and `filter` return **generators** so their direct substitue is a generator expression
* Examples
  * `list(map(factorial, range(6)))` -> `[factorial(n) for n in range(6)]`
  * `list(map(factorial, filter(lambda x: x % 2, range(6))))` -> `[factorial(n) for n in range(6) if n % 2]`
* `reduce` was demoted from a built-in in Python 2 to the `functools` module in Python 3.
  * `reduce` can be replaced by `sum` (other reducing built-ins are `all` and `any`)
  * `reduce(add, range(100))` -> `sum(range(100))`

## 4. Anonymous Functions
* `lambda` creates an anonymous function
* The best use of `lambda` is for an argument list for a **higher-order function**.
    ```python
    names = ["Jason", "Bob", "Jack", "Alice"]
    sorted(names, key=lambda word: word[::-1])
    ```
* Anonymous functions are **rarely used** in Python.
  * If a `lambda` is hard to read, refactor to `def` function.
  * Fredrik Lundh's refactoring advice for Lambda 🤣
    1. Write a comment explaning what the heck the `lambda` does
    2. Study the comment for a while, and think of a name that captures the essence of the comment
    3. Convert the `lambda` to a `def` statement, using that name
    4. Remove the comment.
  * In summary, don't use lambda in most cases.

## 5. The Nine Flavors of Callable Objects
* The call operator `()` may be applied to other callable objects besides functions.
* To check whether an object is callable, use `callable()` built-in function.
* As of Python 3.9, there're **9 callable types**
    1. **User-defined functions**: `def` or `lambda`
    3. **Built-in functions**: Functions implemented in `C` (for CPython) like `len` and `time.strftime`
    4. **Built-in methods**: `dict.get()`
    5. **Methods**
    6. **Classes**: When invoked, a class runs its `__new__` method to create an instance, then `__init__` to initialize it. 
    7. **Class instances**: If a class defines a `__call__` method, its instances may be invoked
    8. **Generator functions**: Functions/methods that use `yield` keyword in the body. When called, return a generator object.
    9. **Native coroutine functions**: Functions/methods defined with `async def`. When called, they return a coroutine object. Added in Python 3.5
    10. **Asynchronous generator functions**: Functions/methods defined with `async def` that have `yield` in their body. When called, they return an asynchronous generator for use with `async for`.

## 6. User-Defined Callable Types

```python
class Person:
    def __init__(self, name):
        self.name = name

    def __call__(self):
        print(f"Hello, I'm {self.name}!")


p = Person("jason")
p() # Hello, I'm jason!
print(callable(p)) # True
```

* Arbitrary Python objects can behave like functions when implementing `__call__` instance method.
* Another use case of `__call__` is **decorator**.


## 7. From Positional to Keyword-Only Paramaters
* `*` and `**` to handle parameters
* To specify keyword-only arguments, name them after the argument prefixed with `*`
* If don't want to support variable positional arguments but want keyword-only arguments, put a `*` by itself in the signature.
  * Keyword-only arguments do not need to have a default value like the example below.
  ```python
  def f(a, *, b):
    return a, b
  >>> f(1, b=2) # (1, 2)
  >>> f(1, 2) # error
  ```


## 8. Positional-Only Parameters

* Since Python 3.8, user-defined functions can have positional-only arguments
* Use `/` to define a function requiring positional-only arguments.
  ```python
  def f(a, b, /):
    return a * b
  ```
  All the params before `/` are positional-only arguments.


## 9. Packages for Functional Programming

### `operator` module <!-- omit from toc -->
* It's often convenient to use an arithmetic operator as a function. (Ex. Multiply a list of numbers)
* To perform summation, we have `sum` but we don't have an equivalent for multiplication. We can use `reduce` but then we would have to implement a multiplication function.
* Instead we can use `mul` function from `operator` module.
  ```python
  from functools import reduce
  from operator import mul

  def factorial(n):
    return reduce(mul, range(1, n + 1))
  ```
* We can use `operator` module to **pick items** from or **read attributes** from objects using `itemgetter` and `attrgetter`.
  ```python
  metro_data = [
    ('Tokyo', 'JP', 36.934),
    ('Seoul', 'KR', 340.23),
    ('Mexico City', 'MX', 20.142)
  ]

  from operator import itemgetter
  for city in sorted(metro_data, key=itemgetter(1)): 
    print(city)
  ```
  * We can also pass multiple index args to `itemgetter`, then it returns tuples with the extract values. (ex. `intemgetter(1, 0)`)
* `itemgetter` uses `[]` operator so it can be used for any object that implements `__getitem__`
* A sibling is `attrgetter` which creates functions to extract object attributes **by name**.


## 10. Freezing Arguments with `functools.partial`
* What `partial` does is given a callable, it produces a new callable with some of the args of the original callable bound to predetermined values.
```python
from operator import mul
from functools import partial
triple = partial(mul, 3) # predetermined arg 3
>>> triple(7) # 21
>>> list(map(triple, range(1, 10))) # [3, 6, 9, 12, 15, 18, 21, 24, 27]
```