"""This module provides functionality for a set-like object operation.
"""
from __future__ import annotations
from collections import OrderedDict
from pycinante.types import Set, T, Iterable, Iterator

__all__ = [
    'OrderedSet'
]

class OrderedSet(Set[T]):
    """A set which keeps the ordering of the inserted items. Ref: https://github.com/flag-
    -go/pydu/blob/master/pydu/set.py.

    >>> s = OrderedSet([1, 2, 3])
    >>> s
    OrderedSet({1, 2, 3})
    >>> s.add(4)
    >>> s.add(1)
    >>> s
    OrderedSet({1, 2, 3, 4})
    >>> {1, 2, 3, 4} == s
    True
    >>> list(s)
    [1, 2, 3, 4]
    """

    def __init__(self, iterable: Iterable[T] | None = None) -> None:
        super(OrderedSet, self).__init__()
        self.data = OrderedDict.fromkeys(iterable or ())

    def add(self, element: T) -> None:
        self.data[element] = None

    def remove(self, element: T) -> None:
        del self.data[element]

    def discard(self, element: T) -> None:
        try:
            del self.data[element]
        except KeyError:
            pass

    def __iter__(self) -> Iterator[T]:
        for element in self.data.keys():
            yield element

    def __contains__(self, element: T) -> bool:
        return element in self.data

    def __bool__(self) -> bool:
        return bool(self.data)

    def __nonzero__(self) -> bool:
        return bool(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __eq__(self, other: ...) -> bool:
        if isinstance(other, OrderedSet):
            return self.data.keys() == other.data.keys()
        return self.data.keys() == other

    def __repr__(self):
        return f'OrderedSet({{{", ".join([repr(e) for e in self.data.keys()])}}})'
