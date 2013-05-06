#!/usr/bin/env python
# -*- coding: utf-8 -*-
from promise import Deferred
from functools import wraps


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
