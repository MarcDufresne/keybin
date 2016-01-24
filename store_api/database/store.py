from __future__ import absolute_import

import re
from functools import wraps

from store_api import config
from store_api.database.mongo import Mongo
from store_api.errors import Error


def validate_key(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        import inspect
        args_name = inspect.getargspec(function)[0]
        args_dict = dict(zip(args_name, args))
        if not re.match(r'^[a-zA-Z0-9_\.,]+$', args_dict[Store.KEY]):
            raise Error(
                code=400,
                message="Key must contain only alphanumeric or _ . , characters"
            )
        return function(*args, **kwargs)
    return wrapper


class Store(object):

    KEY = 'key'
    VALUE = 'value'
    USER_ID = 'user_id'

    def __init__(self):
        self.store = Mongo(config.MONGO_STORE_COLLECTION)

    @validate_key
    def get(self, key, user_id):
        item = self.store.get({self.KEY: key, self.USER_ID: user_id})
        if item:
            return item.get(self.VALUE)
        else:
            raise Error(code=404, message="Key '{}' not found".format(key))

    def get_all_keys(self, user_id):
        items = self.store.find_all({self.USER_ID: user_id})

        keys = []
        for item in items:
            keys.append(item.get(self.KEY))
        return keys

    @validate_key
    def set(self, key, value, user_id):
        self.store.upsert(
            {self.KEY: key, self.USER_ID: user_id},
            {
                self.KEY: key,
                self.VALUE: value,
                self.USER_ID: user_id,
            }
        )

    @validate_key
    def delete(self, key, user_id):
        self.store.delete({self.KEY: key, self.USER_ID: user_id})

    def delete_all(self, user_id):
        self.store.delete_all({self.USER_ID: user_id})
