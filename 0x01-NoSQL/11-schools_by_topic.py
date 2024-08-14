#!/usr/bin/env python3

"""Returns the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """Returns the list of school having a specific topic

    Args:
        mongo_collection: The mongo db collection object
        topic: The topic to use for filtering documents in the collection
    """
    return list(mongo_collection.find({'topics': {'$in': [topic]}}))
