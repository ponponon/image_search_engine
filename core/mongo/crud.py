import pymongo
from core.mongo.models import collection


def insert_one(doc: dict) -> bool:
    collection.insert_one(doc)
    return True
