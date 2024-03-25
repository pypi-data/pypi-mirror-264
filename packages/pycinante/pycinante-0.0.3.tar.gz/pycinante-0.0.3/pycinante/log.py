"""This module provides functionality for logging conveniently.
"""
from __future__ import annotations
import sys
import logging
from loguru import logger
from typing import AnyStr

__all__ = [
    'CRITICAL',
    'FATAL',
    'ERROR',
    'WARNING',
    'WARN',
    'INFO',
    'DEBUG',
    'NOTSET',
    'logger',
    'debug',
    'info',
    'warning',
    'error',
    'critical',
    'success',
    'disable_console_log',
    'log_to_file'
]

CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

debug = (lambda msg, *args, **kwargs: logger.debug(msg, *args, **kwargs))
info = (lambda msg, *args, **kwargs: logger.info(msg, *args, **kwargs))
warning = (lambda msg, *args, **kwargs: logger.warning(msg, *args, **kwargs))
error = (lambda msg, *args, **kwargs: logger.error(msg, *args, **kwargs))
critical = (lambda msg, *args, **kwargs: logger.critical(msg, *args, **kwargs))
success = (lambda msg, *args, **kwargs: logger.success(msg, *args, **kwargs))

def disable_console_log() -> None:
    """Disable any log messages output to the console."""
    logger.remove(handler_id=None)

def enable_console_log(**kwargs) -> None:
    """Enable any log messages output to the console."""
    logger.add(sys.stderr, **kwargs)

def log_to_file(pathname: AnyStr, **kwargs) -> None:
    """Log messages to the file `pathname`."""
    logger.add(pathname, **kwargs)
