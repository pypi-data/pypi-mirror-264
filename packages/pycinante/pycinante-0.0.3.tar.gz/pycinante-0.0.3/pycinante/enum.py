"""This module provides functionality for enum-related operations.
"""
from __future__ import annotations
from enum import Enum
from typing import Type

__all__ = [
    'enum_of',
    'enum_names',
    'enum_values',
    'enum_items'
]

def enum_of(enum: Type[Enum], value: ...) -> Enum:
    """Return an enum instance from the enum according to its value.

    >>> class MyEnum(Enum):
    ...     E = 'hello world'
    >>> enum_of(MyEnum, 'hello world')
    <MyEnum.E: 'hello world'>
    """
    for member in enum.__members__.values():
        if member.value == value:
            return member
    raise ValueError(f'unknown the enum value {value}')

def enum_names(enum: Type[Enum]) -> list[str]:
    """Return the names of the enum members.

    >>> class MyEnum(Enum):
    ...     E = 'hello world'
    >>> enum_names(MyEnum)
    ['E']
    """
    return list(enum.__members__.keys())

def enum_values(enum: Type[Enum]) -> list[...]:
    """Return the values of the enum members.

    >>> class MyEnum(Enum):
    ...     E = 'hello world'
    >>> enum_values(MyEnum)
    ['hello world']
    """
    return [e.value for e in enum.__members__.values()]

def enum_items(enum: Type[Enum]) -> list[tuple[str, ...]]:
    """Return the items of the enum members.

    >>> class MyEnum(Enum):
    ...     E = 'hello world'
    >>> enum_items(MyEnum)
    [('E', 'hello world')]
    """
    return [(k, v.value) for k, v in enum.__members__.items()]
