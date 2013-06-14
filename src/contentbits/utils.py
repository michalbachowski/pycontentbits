#!/usr/bin/env python
# -*- coding: utf-8 -*-
from promise import Deferred
from functools import wraps


def inject_deferred_return_promise(func):
    """
    Injects new deferred object to wrapped function and returns promise instance (for given deferred)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        d = Deferred()
        kwargs['deferred'] = d
        func(*args, **kwargs)
        return d.promise()
    return wrapper

def as_deferred(func):
    """
    Turns synchronous function so it returns deferred instance
    Handles exceptions and return values
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        d = Deferred()
        try:
            d.resolve(func(*args, **kwargs))
        except Exception as e:
            d.reject(exception=e)
        return d.promise()
    return wrapper
