from __future__ import absolute_import

import pymongo

from keybin import config


class Mongo:

    def __init__(self, collection):
        connection = pymongo.MongoClient(config.MONGO_HOST)
        self.db = connection[config.MONGO_DB]
        self.collection = self.db[collection]

    def expire_after(self, field, seconds):
        self.collection.create_index(field, expireAfterSeconds=seconds)

    def get(self, filters=None):
        items = self.collection.find(filters, {'_id': 0})
        for item in items:
            return item
        else:
            return None

    def find_all(self, filters):
        items = self.collection.find(filters, {'_id': 0})
        return items

    def insert(self, document):
        self.collection.insert(document)

    def upsert(self, filters, document):
        self.collection.replace_one(filters, document, upsert=True)

    def delete(self, filters):
        self.collection.remove(filters)

    def delete_all(self, filters):
        self.collection.delete_many(filters)
