# exact cover in Python/numba using algorithm X

an implementation of Donald Knuth's Dancing Links algorithm X in Python / numba

## Usage

```bash
pip install exact_cover_py
```

```python
from exact_cover_py import exact_covers

problem = np.array([
        [1, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0],  # <--
        [0, 0, 0, 1, 1, 0, 1],
        [0, 0, 1, 0, 1, 1, 0],  # <--
        [0, 1, 1, 0, 0, 0, 1],
        [0, 1, 1, 0, 0, 1, 1],  # <--
        [0, 1, 0, 0, 0, 0, 1],
   ])

# exact_covers returns a generator of solutions

# one solution
print(next(exact_covers(problem)))
[1, 5, 3]

# all solutions
print(list(exact_covers(problem)))
[[1, 5, 3]]

# number of solutions
def mylen(iterable):
    return sum(map(lambda x: 1, iterable))

print(mylen(exact_covers(problem)))
2
```
