"""This module provides functionality for a dict-like object operation.
"""
from __future__ import annotations
from collections import OrderedDict
from pycinante.types import Callable, Dict, K, V, Iterable, Type, Iterator
from pycinante.validator import require_variable_name, require_optional_type

__all__ = [
    'update',
    'optional_factory',
    'DefaultDict',
    'AttrDict',
    'attrify',
    'OrderedDict'
]

def update(
    d: dict | None = None,
    m: dict | None = None,
    condition: Callable[[tuple[..., ...]], bool] | None = None,
    **kwargs
) -> dict[..., ...]:
    """Update the dict in place and return itself with new items.

    >>> d = {'a': 1, 'b': 2}
    >>> update(d, {'c': 3, 'd': 4})
    {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    >>> update(d, e=5)
    {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
    """
    m = m or {}
    m.update(**kwargs)
    condition = condition or (lambda _: True)
    m = dict(filter(lambda kv: condition(kv), m.items()))
    d = d or {}
    d.update(m)
    return d

def optional_factory() -> None:
    """Return None rather than raise KeyError if the key is not present in the dict.

    >>> assert optional_factory() is None
    """
    return None

class DefaultDict(Dict[K, V]):
    # noinspection PyTypeChecker
    """A default factory dictionary has default value with default factory. Namely, the d-
    -efault will be returned when the key is not present in a dict. But if the factory is
    None, the key error will be raised. Ref: https://github.com/flaggo/pydu/blob/master/p-
    -ydu/dict.py.

    Args:
        factory (Callable[[], Any]): when a key does not exist in the dictionary, return
        the value returned by the factory method.
        args (Mapping, Iterable): new dictionary initialized from a mapping object's k-v
        pairs.
        kwargs (Mapping): new dictionary initialized with the name=value pairs.

    >>> d = DefaultDict(optional_factory)
    >>> assert d.get('foo') is None
    >>> d['foo'] = 'bar'
    >>> assert d.get('foo') == 'bar'
    >>> import pickle
    >>> pickle.loads(pickle.dumps(d))
    DefaultFactoryDict(optional_factory, {'foo': 'bar'})
    >>> assert id(d.copy()) != id(d)
    >>> from copy import deepcopy
    >>> assert id(deepcopy(d)) != id(d)
    """
    def __init__(
        self,
        factory: Callable[[], ...] | None = None,
        *args: Iterable[Iterable[K, V]],
        **kwargs: dict[K, V]
    ) -> None:
        self.factory = require_optional_type(factory, Callable)
        super(DefaultDict, self).__init__(*args, **kwargs)

    def __getitem__(self, key: K) -> V:
        try:
            return super(DefaultDict, self).__getitem__(key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key: K) -> V:
        if self.factory is None:
            raise KeyError(key)
        self[key] = value = self.factory()
        return value

    def __reduce__(self) -> tuple[Type[DefaultDict], tuple, None, None, Iterator]:
        args = (self.factory,) if self.factory else ()
        return type(self), args, None, None, iter(self.items())

    def __repr__(self) -> str:
        return (f'DefaultFactoryDict({self.factory.__name__}, '
                f'{super(DefaultDict, self).__repr__()})')

    def __copy__(self) -> 'DefaultDict':
        return self.__class__(self.factory, self)

    def copy(self) -> 'DefaultDict':
        return self.__copy__()

    def __deepcopy__(self, memo) -> 'DefaultDict':
        from copy import deepcopy
        return self.__class__(self.factory, deepcopy(iter(self.items())))

class AttrDict(Dict[str, V]):
    """An attribute dictionary that allows accessing dictionary values as if accessing cl-
    -ass attributes. e.g. d['foo'] can be accessed same as d.foo. It requires all key nam-
    -es must be valid variable names. Ref: https://github.com/makinacorpus/easydict, http-
    -s://flaggo.github.io/pydu/#/zh-cn/dict?id=dictattrdict.

    Args:
        d (Dict[str, Any]): new dictionary initialized from a mapping object's k-v pairs.
        factory (Callable[[], Any]): when a key does not exist in the dictionary, return
        the value returned by the factory method.
        kwargs (Dict[str, Any]): the key-value pairs passed through kwargs will be used t-
        -ogether with d as the initial dictionary.

    >>> d = AttrDict({'foo': 'bar'})
    >>> assert d['foo'] == d.foo
    >>> d['animal.cat.kitty'] = 'pikachu'
    >>> assert d['animal.cat.kitty'] == d.animal.cat.kitty
    >>> d
    {'foo': 'bar', 'animal': {'cat': {'kitty': 'pikachu'}}}
    """
    def __init__(
        self,
        d: dict[str, V] | Iterable[Iterable[str, V]] | None = None,
        factory: Callable[[], V] | None = None,
        **kwargs: V
    ) -> None:
        super(AttrDict, self).__init__()
        self.update(d, **kwargs)
        self.factory = require_optional_type(factory or optional_factory, Callable)

    def __setattr__(self, key: str, value: V) -> None:
        """Set the value associated with the key in the dict."""
        key = require_variable_name(key)
        if isinstance(value, (list, tuple)):
            t = [(isinstance(e, dict) and self.__class__(e)) or e for e in value]
            value = type(value)(t)
        elif isinstance(value, dict) and not isinstance(value, AttrDict):
            value = self.__class__(value)
        super(AttrDict, self).__setattr__(key, value)
        super(AttrDict, self).__setitem__(key, value)

    def __setitem__(self, key: str, value: V) -> None:
        """Set the value associated with the key in the dict. You can use the chain key
        (e.g. k1.k2.k3.k4) to set the value associated with the key `d.k1.k2.k3.k4`.
        """
        keys, obj = key.split('.'), self
        for k in keys[:-1]:
            obj.__setattr__(k, {})
            obj = obj.__getattr__(k)
        obj.__setattr__(keys[-1], value)

    def __getattr__(self, key: str) -> V:
        """Return the value associated with the key from the dict."""
        try:
            return super(AttrDict, self).__getitem__(key)
        except KeyError:
            return self.__missing__(key)

    def __getitem__(self, key: str) -> V:
        """Return the value associated with the key from the dict. You can use the chain key
        (e.g. k1.k2.k3.k4) to get the value associated the key `d.k1.k2.k3.k4`.
        """
        value = self
        for k in key.split('.'):
            assert value is not None and isinstance(value, AttrDict), \
                f'the key {key} is not a valid key'
            value = value.__getattr__(k)
        return value

    def __missing__(self, key: str) -> V:
        if self.factory is None:
            raise KeyError(key)
        self[key] = value = self.factory()
        return value

    def update(
        self,
        d: dict[str, V] | Iterable[Iterable[str, V]] | None = None,
        **kwargs: V
    ) -> None:
        """Update the dict with the key/value pairs from other, overwriting existing keys.
        """
        d = d or {}
        d = (isinstance(d, Iterable) and dict(d)) or d
        for key, value in update(d, kwargs).items():
            self.__setattr__(key, value)

    def pop(self, key: str, default: V | None = None) -> V:
        """Remove and return an arbitrary element from the set."""
        delattr(self, key)
        return super(AttrDict, self).pop(key, default)

    def __repr__(self) -> str:
        return '{' + ', '.join(
            [f'{k.__repr__()}: {v.__repr__()}'
             for k, v in self.items()
             if k not in ('factory',)]
        ) + '}'

def attrify(
    d: dict[str, V] | None, factory: Callable[[], V] | None = None, **kwargs: V
) -> AttrDict[V]:
    # noinspection PyUnresolvedReferences
    """Return an object of type AttrDict, which encapsulates the dictionary object d and
    the key-value pairs from kwargs. Ref: https://github.com/flaggo/pydu/blob/master/pydu-
    -/dict.py.

    >>> d = attrify({'a': 1, 'b': {'c': [1, 2, 3]}})
    >>> assert d.b.c[2] == 3
    """
    return AttrDict(d, factory, **kwargs)
