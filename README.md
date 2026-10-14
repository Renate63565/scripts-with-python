# scripts-with-python

A small, dependency-free Python implementation of a Bag (multiset) — an
unordered collection that tracks how many copies of each element it holds.

```python
from scripts_with_python import Bag

b = Bag(["apple", "apple", "pear"])
b.insert("apple")
print(b.count("apple"))   # 3
b.remove("apple", 2)
print(b.count("apple"))   # 1
print("pear" in b)        # True
```

## Why this exists

`collections.Counter` can store arbitrary integer values, including negatives
and zero-valued keys. That flexibility is useful for tallying but makes it a
poor fit when you need a strict multiset invariant: every element has a
positive count, and removing more copies than exist is an error, not a silent
clamp. `Bag` enforces that invariant directly, so bugs that would silently
degrade a `Counter` into a negative-tally mess surface immediately.

The trade-off is that `Bag` is intentionally narrower. It does not support
arithmetic between bags, negative counts, or set-theoretic operations. If you
need those, `Counter` is the right tool.

## Edge case

`bool` is a subclass of `int`, so `insert("a", True)` would be accepted by a
naive `isinstance(times, int)` check and treated as adding one copy. `Bag`
rejects `bool` explicitly via `TypeError`, because passing a boolean where a
count is expected is almost always a caller mistake.
