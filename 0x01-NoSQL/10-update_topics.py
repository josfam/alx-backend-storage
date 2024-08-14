#!/usr/bin/env python3

"""Changes all topics of a school document based on the name"""


def update_topics(mongo_collection, name, topics):
    """Changes all topics of a school document based on the name

    Args:
        mongo_collection: The mongo db collection object
        name: The name of the target documents to change
        topis: The new topics to give the matching document
    """
    # extract collections with a matching name
    mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})
