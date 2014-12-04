import os
from functools import wraps
from requests import Timeout, ConnectionError
from socket import timeout as socket_timeout
import logging
from .models import ArbitraryAccessObject
from shutil import get_terminal_size

timeouts = (Timeout, socket_timeout, ConnectionError)

__author__ = 'zz'


def threading_lock(lock):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper
    return decorator


def retry_connect(retry_times, timeout, error=None):
    if error is None:
        error = ArbitraryAccessObject()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try_times = 0
            while True:
                try:
                    ret = func(*args, timeout=timeout, **kwargs)
                    if ret.status_code != 200:
                        logging.warning('%s is %s', ret.url, ret.status_code)

                except timeouts:
                    try_times += 1
                    error.reconnect(try_times)

                else:
                    return ret

                if try_times >= retry_times:
                    raise Timeout

        return wrapper
    return decorator


def semalock(s):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with s:
                return func(*args, **kwargs)
        return wrapper
    return decorator


def loop(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            ret = func(*args, **kwargs)
            if ret:
                break
    return wrapper


def resolve_timeout(replace_value):
    """
    return replace value instead of raise timeout
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except timeouts as e:
                return replace_value
        return wrapper
    return decorator


def clear_output(func):
    terminal_width, _ = get_terminal_size()

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(' ' * terminal_width, end='\r')
        return func(*args, **kwargs)
    return wrapper


def prepare_dir(dirname):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not os.path.exists(dirname):
                os.mkdir(dirname)

            return func(*args, **kwargs)
        return wrapper
    return decorator