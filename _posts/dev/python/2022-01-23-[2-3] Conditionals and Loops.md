---
title: "Conditionals and Loops"
categories: [Dev, Python]
tags: deployment
math: true
---


## Compare Operators

<code>x == y</code>: value

<code>x is y</code>: value and memory

```python
a = [1, 2, 3, 4, 5]
b = [1, 2, 3, 4, 5]
print(a == b)
print(a is b)
```

<pre>
True
False
</pre>

**[Important]** There's reserved memory space -5 ~ 256 (shared memory)

```python
a = 256
b = 256
print(a == b)
print(a is b)
```

<pre>
True
True
</pre>

```python
a = 257
b = 257
print(a == b)
print(a is b)
```

<pre>
True
False
</pre>

## True and False

- <code>int</code>: <code>1</code> **True**, else False

- <code>str</code>: <code>""</code> **False**, else True

<code>all()</code> <code>any()</code>

```python
b = [True, False, True]
print(all(b)) # AND - True if everything is true
print(any(b)) # OR - True of any is true
```

<pre>
False
True
</pre>

## for

<code>for i in range(x,y,z)</code>: increment by <code>z</code> from <code>x</code> to <code>y-1</code>

```python
for i in range(2, 10, 2): # [2,10) +2
    print(i, end="")
print("\n")
for i in range(11, 1, -2): # [11, 1) -2
    print(i, end="")
```

<pre>
2468

119753
</pre>

```python

```
