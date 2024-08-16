#!/usr/bin/env python3

"""A Cache class that mimics a cache, leveraging redis as a foundation"""

import redis
from uuid import uuid4
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Counts how many times methods of the Cache class are called"""

    # inner function
    @wraps(method)
    def wrapper(*args, **kwargs):
        self = args[0]  # self is the first argument
        self._redis.incr(method.__qualname__)
        return method(*args, **kwargs)

    return wrapper


class Cache:
    """Represents a cache, using redis as a base"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generates a random key, stores the input data in Redis using the
        random key and returns the key.

        Args:
            data: The data to store as a value of the randomly generated key
        Returns:
            The randomly generated key
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Union[Callable, None] = None
    ) -> Union[str, bytes, int, float, None]:
        """Returns the value belonging to this key in the cache, and uses the
        optional callable provided to turn the value into the desired format.

        Args:
            key: The key whose value to retrieve
            fn: Optional callable used to convert the data to a desired format.
        Returns:
            The value as is, or as dictated by the callable. None if the key
            did not exist in the first place.
        """
        value = self._redis.get(key)
        if value is None:
            return None  # replicate redis' behavior

        if fn is None:
            return value
        else:
            return fn(value)

    def get_str(self, key: str) -> Union[str, None]:
        """Gets back the string representation of the value whose key
        is provided

        Args:
            key: The key whose value to retrieve as a string
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Union[str, bytes, int, float, None]:
        """Gets back the integer representation of the value whose key
        is provided

        Args:
            key: The key whose integer representation to retrieve
        """
        return self.get(key, lambda x: int(x.decode('utf-8')))
