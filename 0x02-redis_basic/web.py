#!/usr/bin/env python3

"""Caches web requests, and sets an expiration on the cached result"""

import requests
import redis


def get_page(url: str) -> str:
    """Makes a request for a web page, and uses the cached contents if the
    url was visited before
    """
    pass
