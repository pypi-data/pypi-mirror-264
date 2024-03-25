# Sequence Edits

> Tools for encoding/decoding sequence editions (insertions/deletions) in compact forma

## Edits

```python
class Skip:
    idx: int

class Insert:
    idx: int
    value: T
```

All edits are applied w.r.t. the original list. So, order of edits only affects the order in which values are insterted to a same index.

## Usage

```python
import sequence_edits as se

edits = [
    se.Insert(idx=1, value='the'),
    se.Skip(idx=4)
]
xs = ['And',      'earth', 'was', 'without', 'no', 'form']
list(se.apply(edits, xs))
#  ['And', 'the', 'earth', 'was', 'without',       'form']
```