---
title: "[Fluent Python] Ch7. Functions as First-Class Objects"
categories: [Dev, Python]
math: true
---

## Table of Contents <!-- omit from toc -->
- [1. Treating a Function Like an Object](#1-treating-a-function-like-an-object)
- [2. Higher-Order Functions](#2-higher-order-functions)
- [3. List Comprehension: Modern Replacement for map, filter, and reduce](#3-list-comprehension-modern-replacement-for-map-filter-and-reduce)
- [3. Anonymous Functions](#3-anonymous-functions)
- [The Nine Flavors of Callable Objects](#the-nine-flavors-of-callable-objects)

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

## 3. Anonymous Functions
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

## The Nine Flavors of Callable Objects
* The call operator `()` may be applied to other callable objects besides functions.
* To check whether an object is callable, use `callable()` built-in function.
* As of Python 3.9, there're **9 callable types**
    1. User-defined functions
    2. Built-in functions