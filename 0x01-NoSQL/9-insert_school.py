#!/usr/bin/env python3

"""Function that inserts a new document into a collection using key word
arguments
"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in a collection based on kwargs

    Args:
        mongo_collection: The mongo db collection object

    Returns:
        The unique id of the inserted document
    """
    inserted = mongo_collection.insert_one(dict(kwargs)).inserted_id
    return inserted
