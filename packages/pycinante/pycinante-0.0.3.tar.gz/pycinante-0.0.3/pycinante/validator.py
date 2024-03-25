"""This module provides functions to validate a given values.
"""
from __future__ import annotations
from functools import wraps
import math
import re
import os
from pycinante.types import Sized, T, U, Union, Callable, Number, Type, Optional

__all__ = [
    'require_not_empty',
    'require_gt',
    'require_gt_0',
    'require_ge',
    'require_lt',
    'require_le',
    'require_eq',
    'require_between',
    'require_probability',
    'require_regex',
    'require_variable_name',
    'require_not_none',
    'require_not_none_else',
    'require_not_empty_else',
    'require_type',
    'require_optional_type',
    'require_exists',
    'require_a_file',
    'require_a_directory',
    'check_condition',
    'check_positional_arguments',
    'check_not_empty',
    'check_gt',
    'check_gt_0',
    'check_ge',
    'check_lt',
    'check_le',
    'check_eq',
    'check_between',
    'check_probability',
    'check_regex',
    'check_variable_name',
    'check_not_none',
    'check_not_none_else',
    'check_not_empty_else',
    'check_type',
    'check_optional_type'
]

def is_empty(obj: ...) -> bool:
    """Return whether the object `obj` is empty."""
    if obj is None:
        return True
    if isinstance(obj, Sized):
        return len(obj) == 0
    if getattr(obj, '__empty__', None) is not None:
        return getattr(obj, '__empty__')()
    return False

def where(condition: bool, obj: T, other: U) -> Union[T, U]:
    """Return the first object if the condition is True otherwise return the second."""
    return obj if condition else other

def require_not_empty(
    obj: T,
    checker: Callable[[...], bool] | None = None,
    msg: str | None = None
) -> T:
    """Check whether the object `obj` is not empty."""
    checker = checker or (lambda e: not is_empty(e))
    assert checker(obj), msg or 'the obj must be not empty'
    return obj

def require_not_empty_else(
    obj: T,
    other: U,
    checker: Callable[[...], bool] | None = None
) -> T | U:
    """Return the `obj` if the `obj` is not empty otherwise return the `other`."""
    checker = checker or (lambda e: not is_empty(e))
    return obj if not checker(obj) else other

def require_gt(val: Number, min_val: Number, msg: str | None = None) -> Number:
    """Check whether the `val` is greater than the value `min_val`."""
    assert val > min_val, msg or f'the value {val} must be greater than {min_val}'
    return val

def require_gt_0(val: Number, msg: str | None = None) -> Number:
    """Check whether the `val` is greater than the value 0."""
    assert val > 0, msg or f'the value {val} must be greater than 0'
    return val

def require_ge(
    val: Number, min_val: Number, epsilon: float = 1e-6, msg: str | None = None
) -> Number:
    """Check whether the `val` is greater than or equal to the value `min_val`."""
    msg = msg or f'the value {val} must be greater than or equal to {min_val}'
    assert val > min_val or abs(val - min_val) < epsilon, msg
    return val

def require_lt(val: Number, max_val: Number, msg: str | None = None) -> Number:
    """Check whether the `val` is less than the value `max_val`."""
    assert val < max_val, msg or f'the value {val} must be less than {max_val}'
    return val

def require_le(
    val: Number, max_val: Number, epsilon: float = 1e-6, msg: str | None = None
) -> Number:
    """Check whether the `val` is less than or equal to the value `max_val`."""
    msg = msg or f'the value {val} must be less than or equal to {max_val}'
    assert val < max_val or abs(val - max_val) < epsilon, msg
    return val

def require_eq(
    val: Number, eq_val: Number, epsilon: float = 1e-6, msg: str | None = None
) -> Number:
    """Check whether the `val` is equal to the value `eq_val`."""
    msg = msg or f'the value {val} must be equal to {eq_val}'
    assert abs(val - eq_val) < epsilon, msg
    return val

def require_between(
    val: Number,
    min_val: Number = -math.inf,
    max_val: Number = math.inf,
    epsilon: float = 1e-6,
    msg: str | None = None
) -> Number:
    """Check whether the value `val` is in the range `min_val` (included) and `max_val`
    (included).
    """
    msg = msg or f'the value {val} must be between {min_val} and {max_val}'
    assert (min_val < val < max_val or abs(val - min_val) < epsilon or
            abs(val - max_val) < epsilon), msg
    return val

def require_probability(val: Number, msg: str | None = None) -> Number:
    """Check whether the value `val` is between 0. and 1."""
    msg = msg or f'the probability value {val} must be between 0. and 1.'
    return require_between(val, 0, 1, msg=msg)

def require_regex(val: str, pattern: str, msg: str | None = None) -> str:
    """Check whether the string `val` matches the regular expression."""
    msg = msg or f'the string {val} is not matching the regular expression {pattern}'
    assert re.match(pattern, val), msg
    return val

def require_variable_name(val: str, msg: str | None = None) -> str:
    """Check whether the variable name `val` is a valid variable name."""
    msg = msg or f'the variable {val} is not a valid variable name'
    return require_regex(val, r'^[a-zA-Z_][a-zA-Z0-9_]*$', msg)

def require_not_none(obj: T, msg: str | None = None) -> T:
    """Check whether the `obj` is not none."""
    assert obj is not None, msg or f'the obj must be not None'
    return obj

def require_not_none_else(obj: T, other: U) -> T | U:
    """Return the `obj` if the `obj` is not None otherwise return the `other`."""
    return obj if obj is not None else other

# validating for object types

def is_type(obj: ..., types: Type | tuple[Type]) -> bool:
    """Check whether the `obj` is an instance of the `types` type."""
    return isinstance(obj, types)

def is_optional_type(obj: ..., types: Type | tuple[Type]) -> bool:
    """Check whether the `obj` is an instance of the `types` type or None."""
    return obj is None or isinstance(obj, types)

def is_none(obj: ...) -> bool:
    """Check whether the `obj` is an instance of the none type."""
    return obj is None

def require_none(obj: T, msg: str | None = None) -> T:
    """Check whether the `obj` is an instance of the none type."""
    return obj is None

def is_integer(obj: ...) -> bool:
    """Check whether the `obj` is an instance of the int type."""
    return isinstance(obj, int)

def is_float(obj: ...) -> bool:
    """Check whether the `obj` is an instance of the float type."""
    return isinstance(obj, float)

def is_number(obj: ...) -> bool:
    """Check whether the `obj` is an instance of the number type."""
    return isinstance(obj, (int, float))

def is_string(obj: ...) -> bool:
    """Check whether the `obj` is an instance of the string type."""
    return isinstance(obj, (str, bytes))

def is_boolean(obj: ...) -> bool:
    """Check whether the `obj` is an instance of the boolean type."""
    return isinstance(obj, bool)

def is_dictionary(obj: ...) -> bool:
    """Check whether the `obj` is an instance of the dictionary type."""
    return isinstance(obj, dict)

def is_tuple(obj: ...) -> bool:
    """Check whether the `obj` is an instance of the tuple type."""
    return isinstance(obj, tuple)

def is_list(obj: ...) -> bool:
    """Check whether the `obj` is an instance of the list type."""
    return isinstance(obj, list)

def is_array(obj: ...) -> bool:
    """Check whether the `obj` is an instance of the array type."""
    return isinstance(obj, (list, tuple, set))

def is_set(obj: ...) -> bool:
    """Check whether the `obj` is an instance of the set type."""
    return isinstance(obj, set)

def require_type(obj: T, types: Type | tuple[Type], msg: str | None = None) -> T:
    """Check whether the `obj` is an instance of the `types` type."""
    assert is_type(obj, types), msg or f'the type of `obj` must be the type {types}'
    return obj

def require_optional_type(
    obj: Optional[T],
    types: Type | tuple[Type],
    msg: str | None = None
) -> Optional[T]:
    """Check whether the `obj` is an instance of the `types` type or None."""
    assert is_optional_type, msg or f'the type of `obj` must be the type {types} or None'
    return obj

# validating for file

def require_exists(pathname: str, msg: str | None = None) -> str:
    """Check whether the `pathname` refers to an existing path."""
    msg = msg or f'the path {pathname} must refer to an existing path'
    assert os.path.exists(pathname), msg
    return pathname

def require_a_file(pathname: str, msg: str | None = None) -> str:
    """Check whether the `pathname` is an existing regular file."""
    msg = msg or f'the path {pathname} must be an existing regular file'
    assert os.path.isfile(pathname), msg
    return pathname

def require_a_directory(pathname: str, msg: str | None = None) -> str:
    """Check whether the `pathname` is an existing directory."""
    msg = msg or f'the path {pathname} must be an existing directory'
    assert os.path.isdir(pathname), msg
    return pathname

# annotation checker

def check_condition(
    condition: Union[bool, Callable[[], bool]],
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Check whether the condition is supported.

    Args:
        condition (bool, Callable): boolean condition or a predictor.
        msg (str, optional): error message.
    """
    if isinstance(condition, Callable):
        condition = condition()

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> ...:
            assert condition, msg or 'the condition is not supported'
            return func(*args, **kwargs)
        return wrapper
    return decorator

def check_positional_arguments(
    validator: Callable,
    index: int | list[int] | Callable,
    **params: ... | None
) -> Callable[[Callable], Callable]:
    """Check whether an argument at specified position on the function list is valid.

    Args:
        index (int, List[int], Callable): specifies the index of the argument being check-
        -ed when the type of the index is int or List[int]; Otherwise it represents the d-
        -ecorated function and in which case the default index of the argument being chec-
        -ked is 0. params (dict): the parameters of the validator to be called.
    """
    # the default index of the argument being checked is 0
    index = require_not_none_else(index, [0])
    indexes = where(isinstance(index, Callable), [0],
                    (isinstance(index, int) and [index] or index))

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> ...:
            return func(*[validator(args[i], **(params or {})) for i in indexes],
                        **kwargs)
        return wrapper

    if isinstance(index, Callable):
        # for annotation without arguments
        return decorator(index)
    return decorator

def check_not_empty(
    index: int | list[int] | Callable | None = None,
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Check whether the arguments args[index] is not empty."""
    return check_positional_arguments(require_not_empty, index, msg=msg)

def check_gt(
    min_val: int,
    index: int | list[int] | Callable | None = None,
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Check whether the args[index] is greater than the value `min_val`."""
    params = {'min_val': min_val, 'msg': msg}
    return check_positional_arguments(require_gt, index, min_val=min_val, msg=msg)

def check_gt_0(
    index: int | list[int] | Callable | None = None,
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Check whether the argument args[index] is greater than the value 0."""
    return check_positional_arguments(require_gt_0, index, msg=msg)

def check_ge(
    min_val: int,
    index: int | list[int] | Callable | None = None,
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Check whether the args[index] is greater than or equal to the value `min_val`."""
    return check_positional_arguments(require_ge, index, min_val=min_val, msg=msg)

def check_lt(
    max_val: int,
    index: int | list[int] | Callable | None = None,
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Check whether the args[index] is less than the value `max_val`."""
    return check_positional_arguments(require_lt, index, max_val=max_val, msg=msg)

def check_le(
    max_val: int,
    index: int | list[int] | Callable | None = None,
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Check whether the args[index] is less than or equal to the value `max_val`."""
    return check_positional_arguments(require_le, index, max_val=max_val, msg=msg)

def check_eq(
    eq_val: int,
    index: int | list[int] | Callable | None = None,
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Check whether the args[index] is equal to the value `eq_val`."""
    return check_positional_arguments(require_eq, index, eq_val=eq_val, msg=msg)

def check_between(
    min_val: int,
    max_val: int,
    index: int | list[int] | Callable | None = None,
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Check whether the value args[index] is in the range `min_val` and `max_val`."""
    params = {'min_val': min_val, 'max_val': max_val, 'msg': msg}
    return check_positional_arguments(require_between, index, **params)

def check_probability(
    index: int | list[int] | Callable | None = None,
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Check whether the argument args[index] is between 0. and 1."""
    return check_positional_arguments(require_probability, index, msg=msg)

def check_regex(
    pattern: str,
    index: int | list[int] | Callable | None = None,
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Check whether the string args[index] matches the regular expression."""
    return check_positional_arguments(require_regex, index, pattern=pattern, msg=msg)

def check_variable_name(
    index: int | list[int] | Callable | None = None,
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Check whether the arguments args[index] is a valid variable name."""
    return check_positional_arguments(require_variable_name, index, msg=msg)

def check_not_none(
    index: int | list[int] | Callable | None = None,
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Check whether the argument args[index] is not None."""
    return check_positional_arguments(require_not_none, index, msg=msg)

def check_not_none_else(
    other: int,
    index: int | list[int] | Callable | None = None,
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Return the args[index] if the args[index] is not None otherwise return the `other`.
    """
    return check_positional_arguments(require_not_none_else, index, other=other, msg=msg)

def check_not_empty_else(
    other: int,
    index: int | list[int] | Callable | None = None,
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Return the args[index] if the args[index] is not empty otherwise return the `other`
    .
    """
    return check_positional_arguments(require_not_empty_else, index, other=other, msg=msg)

def check_type(
    types: Type | tuple[Type],
    index: int | list[int] | Callable | None = None,
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Check whether the args[index] is an instance of the `types` type."""
    return check_positional_arguments(require_type, index, types=types, msg=msg)

def check_optional_type(
    types: Type | tuple[Type],
    index: int | list[int] | Callable | None = None,
    msg: str | None = None
) -> Callable[[Callable], Callable]:
    """Check whether the `obj` is an instance of the `types` type or None."""
    return check_positional_arguments(require_optional_type, index, types=types, msg=msg)
