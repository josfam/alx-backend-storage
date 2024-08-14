#!/usr/bin/env python3

"""A Cache class that mimics a cache, leveraging redis as a foundation"""

import redis
from uuid import uuid4
from typing import Union


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
