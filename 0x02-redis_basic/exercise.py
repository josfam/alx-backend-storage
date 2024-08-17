#!/usr/bin/env python3

"""A Cache class that mimics a cache, leveraging redis as a foundation"""

import redis
from uuid import uuid4
from typing import Union, Callable
from functools import wraps


def call_history(method: Callable) -> Callable:
    """Stores the history of inputs and outputs for a particular function"""
    fn_name = method.__qualname__
    inputs = f'{fn_name}:inputs'
    outputs = f'{fn_name}:outputs'

    # inner function
    @wraps(method)
    def wrapper(*args, **kwargs):
        self = args[0]
        # add the inputs
        self._redis.rpush(inputs, str(args[1:]))
        # add the outputs
        output = method(*args, **kwargs)
        self._redis.rpush(outputs, output)
        return output

    return wrapper


def count_calls(method: Callable) -> Callable:
    """Counts how many times methods of the Cache class are called"""
    key = method.__qualname__

    # inner function
    @wraps(method)
    def wrapper(*args, **kwargs):
        self = args[0]  # self is the first argument
        self._redis.incr(key)
        return method(*args, **kwargs)

    return wrapper


class Cache:
    """Represents a cache, using redis as a base"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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


def replay(fn: Callable) -> None:
    """Shows the history of all the inputs and outputs from calling the
    provided function
    """
    fn_name = fn.__qualname__
    local_redis = redis.Redis()
    inputs = f'{fn_name}:inputs'
    outputs = f'{fn_name}:outputs'

    call_count = local_redis.get(f'{fn_name}')
    print(f"{fn_name} was called {call_count.decode('utf-8')} times:")

    inputs = local_redis.lrange(f'{fn_name}:inputs', 0, -1)
    outputs = local_redis.lrange(f'{fn_name}:outputs', 0, -1)

    for input_call, output in zip(inputs, outputs):
        input_str = input_call.decode('utf-8')
        output_str = output.decode('utf-8')
        print(f"{fn_name}(*{input_str}) -> {output_str}")
