"""This module provides functionality for request an HTTP or HTTPS request.
"""
from __future__ import annotations
import requests
from requests import Response
import fake_useragent
from pycinante.dict import update
from pycinante.object import get_default
from pycinante.types import AnyStr

__all__ = [
    'set_request_header',
    'set_request_proxy',
    'get',
    'post'
]

_request_headers = {
    'User-Agent': fake_useragent.UserAgent().chrome
}

def set_request_header(
    key_or_headers: str | dict[str, AnyStr],
    value: AnyStr | None = None
) -> None:
    """Set the global request headers."""
    if isinstance(key_or_headers, str):
        _request_headers[key_or_headers] = value
    elif isinstance(key_or_headers, dict):
        _request_headers.update(key_or_headers)
    raise TypeError(f'Unexpected type {type(key_or_headers)} for `key_or_headers`')

_request_proxies = {}

def set_request_proxy(
    protocol_proxies: str | dict[str, AnyStr],
    host_or_url: str | None = None,
    port: int | None = None
) -> None:
    """Set the global request proxies."""
    if isinstance(protocol_proxies, dict):
        _request_proxies.update(protocol_proxies)
    elif isinstance(protocol_proxies, str):
        if port is None:
            _request_proxies[protocol_proxies] = host_or_url
        else:
            _request_proxies[protocol_proxies] = f'{host_or_url}:{port}'
    raise TypeError(f'Unexpected type {type(protocol_proxies)} for `protocol_proxies`')

def prepare_request(**kwargs: ...) -> dict[str, ...]:
    for key, value in globals().items():
        if key.startswith('_request_'):
            name = key.split('_request_')[-1]
            content = kwargs.pop(name, get_default(value))
            if isinstance(content, dict):
                content = update(content, value, lambda kv: kv[0] not in content)
                kwargs[name] = content
    return kwargs

def get(url: AnyStr, params: ... = None, **kwargs: ...) -> Response:
    kwargs = prepare_request(**kwargs)
    return requests.get(url, params=params, **kwargs)

def post(url: AnyStr, data: ... = None, json: ... = None, **kwargs: ...) -> Response:
    kwargs = prepare_request(**kwargs)
    return requests.post(url, data=data, json=json, **kwargs)
