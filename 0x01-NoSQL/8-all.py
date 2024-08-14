#!/usr/bin/env python3

"""Lists all documents in the provided collection"""


def list_all(mongo_collection):
    """Lists all documents in the provided collection

    Args:
        mongo_collection: The mongo db collection object

    Returns:
        A list of the documents in this collection
    """
    return list(mongo_collection.find())
