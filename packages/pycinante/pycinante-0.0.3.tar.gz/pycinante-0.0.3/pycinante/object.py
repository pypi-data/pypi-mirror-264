"""This module provides functionality for initializing an object.
"""
from __future__ import annotations
from pycinante.types import T, Dict, Type, overload, Iterable
from pycinante.reflect import is_accept_args

__all__ = [
    'NameFactory',
    'get_default'
]

class NameFactory(Dict[str, Type[T]]):
    """Naming Dict used to create an instance given its name.

    >>> factory = NameFactory('int', {'int': int})
    >>> factory.build('int', 5)
    5
    """

    def __init__(self, name: str, d: dict[str, T] | None = None):
        super(NameFactory, self).__init__(d or {})
        self.name = name

    @overload
    def build(self, name: list[str], *args: ..., **kwargs: ...) -> T:
        """Build an instance from the factory with the given instance name and return it.
        """
        pass

    @overload
    def build(self, names: Iterable[str], *args: ..., **kwargs: ...) -> list[T]:
        """Build a group of instances from the factory with the given instance name list
        and return it.
        """
        pass

    def build(self, names: str | Iterable[str], *args: ..., **kwargs: ...) -> T | list[T]:
        """Build an instance or a group of instances from the factory with the given inst-
        -ance name. Note that if the type of names is an iterable, the keyword arguments
        should be {'name': kwargs, ...}, if there is no keyword arguments, just nothing to
        provided in kwargs, e.g. {}. And the args will be passed all the constructor of
        the class when initializing the instance.

        Args:
            names (str | Iterable[str]): the class names to be initialized.
            args (tuple[...]): the positional arguments to be passed to the constructor of
            the class.
            kwargs (dict[str, ...]): the keyword arguments to be passed to the constructor
            of the class.
        """
        if isinstance(names, str):
            if names not in self.keys():
                raise KeyError(f'Unknown name {names} for {self.name}')
            return self[names](*args, **kwargs)
        if isinstance(names, Iterable):
            instances = []
            for name in names:
                if name not in self.keys():
                    raise KeyError(f'Unknown name {name} for {self.name}')
                instances.append(self[name](*args, **kwargs.get(name, {})))
            return instances
        raise TypeError(f'Unsupported type {type(names)}')

    def __str__(self) -> str:
        return f'{self.name} ({super(NameFactory, self).__str__()})'

def get_default(obj: T) -> T:
    """Return a new instance as the same type as the `obj`. A new instance will be instan-
    tiaed by two ways: the first one is instantiated with the `__default__` method if this
    was already implemented in the `obj`; otherwise, the new instance will be created with
    the `__init__` method if any parameters is no needed and in such cases, a TypeError w-
    -ill be raised.

    >>> get_default({1: 2, 'a': 'b'})
    {}
    >>> get_default([1, 2, 3, 4])
    []
    """
    if getattr(obj, '__default__', None) is not None:
        return getattr(obj, '__default__')()
    if is_accept_args(getattr(obj, '__init__')):
        raise TypeError(f'unsupported type {type(obj)} to acquire a default object')
    return type(obj)()
