__author__ = 'zz'

from functools import wraps
from requests import Timeout, ConnectionError
from socket import timeout as socket_timeout
import logging


timeouts = (Timeout, socket_timeout, ConnectionError)




def threading_lock(lock):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper
    return decorator


def retry_connect(retry_times, timeout):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try_times = 0
            while True:
                try:
                    ret = func(*args, timeout=timeout, **kwargs)
                    if ret.status_code != 200:
                        logging.warning('%s is %s', ret.url, ret.status_code)
                        if ret.status_code == 404:
                            raise Timeout

                except timeouts:
                    try_times += 1

                else:
                    return ret

                if try_times >= retry_times:
                    raise Timeout

        return wrapper
    return decorator


def semalock_for_class(func):
    @wraps(func)
    def wrapper(self, s, *args, **kwargs):
        with s:
            return func(self, *args, **kwargs)
    return wrapper


def semalock(func):
    @wraps(func)
    def wrapper(s, *args, **kwargs):
        with s:
            return func(*args, **kwargs)
    return wrapper


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