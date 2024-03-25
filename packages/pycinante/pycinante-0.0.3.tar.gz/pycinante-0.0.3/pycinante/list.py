"""This module provides functionality for a list object accession.
"""
from __future__ import annotations
from pycinante.types import T, Iterable, Callable, Sequence

__all__ = [
    'arange',
    'unique',
    'listify',
    'swap',
    'sort',
    'flatten'
]

def listify(obj: T | Iterable[T]) -> list[T]:
    """Return a list from an object.

    >>> listify('https://www.baidu.com')
    ['https://www.baidu.com']
    >>> listify([1, 2, 3])
    [1, 2, 3]
    >>> listify((1, 2, 3, 2, 1, 2))
    [1, 2, 3, 2, 1, 2]
    >>> listify(iter({4, 5, 6}))
    [4, 5, 6]
    """
    if isinstance(obj, Iterable) and not isinstance(obj, str):
        return list(obj)
    return [obj]

def arange(start: int = 0, stop: int | None = None, step: int = 1) -> list[int]:
    """Return a list of numbers between `start` and `stop` inclusive.

    >>> arange(10)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> arange(1, 10)
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> arange(49, 200, 40)
    [49, 89, 129, 169]
    """
    return list(range((stop and start) or 0, stop or start, step))

def unique(seq: list[T], key: Callable[[T], bool] | None = None) -> list[T]:
    """Removes duplicate elements from a list while preserving the order of the rest.
    Ref: https://github.com/flaggo/pydu/blob/master/pydu/list.py.

    Args:
        seq (list): list to be removed duplicate elements.
        key (Callable): the value of the optional `key` parameter should be a function
        that takes a single argument and returns a key to test the uniqueness.

    >>> unique([1, 2, 3])
    [1, 2, 3]
    >>> unique([1, 2, 1, 3, 3, 2, 1, 2, 3])
    [1, 2, 3]
    """
    key = key or (lambda e: e)
    unique_seq, seen = list(), set()
    for element in seq:
        if key(element) in seen:
            continue
        unique_seq.append(element)
        seen.add(key(element))
    return unique_seq

def swap(
    seq: list[T], i: int | slice | Iterable[int], j: int | slice | Iterable[int]
) -> list[T]:
    """Swap the element of `arr[i]` and `arr[j] in the list `arr`.

    >>> swap([34, 456, 36, 90, 47], 1, 4)
    [34, 47, 36, 90, 456]
    >>> swap([34, 47, 36, 90, 456], slice(0, 2), slice(2, 4))
    [36, 90, 34, 47, 456]
    >>> swap([43, 68, 25, 99, 23, 83], [1, 2, 3], [0, 5, 4])
    [68, 43, 83, 23, 99, 25]
    """
    assert isinstance(i, type(j)), 'the type of `i` and `j` must be the same'
    if isinstance(i, (int, slice)):
        seq[i], seq[j] = seq[j], seq[i]
        return seq
    assert isinstance(i, Sequence), f'the type of {type(i)} is not supported'
    for m, n in zip(i, j):
        seq[m], seq[n] = seq[n], seq[m]
    return seq

def sort(seq: list[T], descending: bool = False) -> list[T]:
    """Sort the list in-place in ascending or descending order and return itself.

    >>> arr = [34, 456, 36, 90, 47, 34, 55, 999, 323]
    >>> sort(seq, False)
    [34, 34, 36, 47, 55, 90, 323, 456, 999]
    >>> sort(seq, True)
    [999, 456, 323, 90, 55, 47, 36, 34, 34]
    """
    seq.sort(reverse=descending)
    return seq

def flatten(seq: Iterable[T]) -> list[T]:
    """Generate each element of the given `seq`. If the element is iterable and is not
    string, it yields each sub-element of the element recursively. Ref: https://github.c-
    -om/flaggo/pydu/blob/master/pydu/list.py.

    >>> flatten([])
    []
    >>> flatten([1, 2, 3])
    [1, 2, 3]
    >>> flatten([0, [1, 2, 3], [4, 5, 6], [7, [8, [9]]]])
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    flatten_seq = []
    for element in seq:
        if isinstance(element, Iterable) and not isinstance(element, (str, bytes)):
            for sub in flatten(element):
                flatten_seq.append(sub)
        else:
            flatten_seq.append(element)
    return flatten_seq
