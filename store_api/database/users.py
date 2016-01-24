from __future__ import absolute_import

from uuid import uuid4

import bcrypt as bcrypt

from store_api import config
from store_api.database.mongo import Mongo
from store_api.errors import Error


class User:

    USERNAME = 'username'
    PASSWORD = 'password'
    USER_ID = 'user_id'

    def __init__(self):
        self.users = Mongo(config.MONGO_USERS_COLLECTION)

    def get(self, username, password):
        user = self.users.get({self.USERNAME: username})
        if user and User.__validate_password(password, user.get('password')):
            del user[self.PASSWORD]
            return user
        else:
            raise Error(code=403, message="Invalid credentials")

    def register(self, username, password):
        if self.users.get({self.USERNAME: username}):
            raise Error(code=409, message="User already registered")

        user_id = str(uuid4())
        self.users.insert(
            {
                self.USER_ID: user_id,
                self.USERNAME: username,
                self.PASSWORD: User.__hash(password)
            }
        )
        return user_id

    def unregister(self, user_id):
        self.validate_user_id(user_id)
        self.users.delete({self.USER_ID: user_id})

    def validate_user_id(self, user_id):
        user = self.users.get({self.USER_ID: user_id})
        if not user:
            raise Error(code=403, message="Invalid user_id")

    @staticmethod
    def __validate_password(input_passwd, user_passwd):
        return user_passwd == User.__hash(input_passwd, salt=user_passwd)

    @staticmethod
    def __hash(password, salt=None):
        def _utf8(s):
            return s.encode('utf-8')

        return bcrypt.hashpw(
            _utf8(password), _utf8(salt) if salt else bcrypt.gensalt())
