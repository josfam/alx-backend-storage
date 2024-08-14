#!/usr/bin/env python3

"""A Cache class that mimics a cache, leveraging redis as a foundation"""

import redis
from uuid import uuid4
from typing import Union, Callable


class Cache:
    """Represents a cache, using redis as a base"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

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

    def get(self, key: str, fn: Union[Callable, None]):
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

        if not fn:
            return value
        else:
            return fn(value)

    def get_str(self, key: str) -> str:
        """Gets back the string representation of the value whose key
        is provided

        Args:
            key: The key whose value to retrieve as a string
        """
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """Gets back the integer representation of the value whose key
        is provided

        Args:
            key: The key whose integer representation to retrieve
        """
        return self.get(key, int)
