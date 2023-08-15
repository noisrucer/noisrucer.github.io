---
title: "Function and Console I/O"
categories: [Dev, Python]
tags: deployment
math: true
---


## formatting output

- <code>%</code>, <code>format</code>, <code>fstring</code>

## <code>%</code>

```python
print('%s %s' % ('hello', 'jason'))
print('%d %s %f' % (10, 'jason', 10.2))
```

<pre>
hello jason
10 jason 10.200000
</pre>

```python
print("%10s" % ("Jason"))
print("%10.5f" % (1/7))
```

<pre>
     Jason
   0.14286
</pre>

```python
print("Name: %(name)10s" % {"name":"jason"})
```

<pre>
Name:      jason
</pre>

## <code>.format()</code>

```python
print('hello {} my name if {}'.format("jason","chilla"))
print('hello {0} my name if {1}'.format("jason","chilla"))
print('hello {0:10.5f} my name if {1}'.format(1/7,"chilla"))
print('hello {you} my name if {me}'.format(you="jason", me="chilla"))
```

<pre>
hello jason my name if chilla
hello jason my name if chilla
hello    0.14286 my name if chilla
hello jason my name if chilla
</pre>

#### padding

```python
print("Name: {:>20.5}".format("Jason"))
```

<pre>
Name:                Jason
</pre>

## <code>fstring</code>

```python
name = "Jason"
age = 26
school = "skrt"
amount = 254.2
print(f"{name:*>20}")
print(f"{name:*<20}")
print(f"{name:*^20}")
print(f"{amount:.2f}")
```

<pre>
***************Jason
Jason***************
*******Jason********
254.20
</pre>
