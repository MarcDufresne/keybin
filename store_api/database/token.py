from datetime import datetime
from uuid import uuid4

from store_api import config
from store_api.database.mongo import Mongo
from store_api.errors import Error


class Token:

    TOKEN = 'token'
    USER_ID = 'user_id'
    CREATED_AT = 'created_at'
    CLIENT_ID = 'client_id'

    DEFAULT_CLIENT_ID = 'default'

    def __init__(self):
        self.token = Mongo(config.MONGO_TOKEN_COLLECTION)
        self.token.expire_after(self.CREATED_AT, config.TOKEN_EXPIRATION)

    def generate(self, user_id, client_id=None):
        token = str(uuid4())
        cid = client_id or self.DEFAULT_CLIENT_ID
        self.token.upsert(
            {
                self.USER_ID: user_id,
                self.CLIENT_ID: cid
            },
            {
                self.TOKEN: token,
                self.USER_ID: user_id,
                self.CREATED_AT: datetime.utcnow(),
                self.CLIENT_ID: cid
            }
        )
        return {
            self.TOKEN: token,
            'expire_seconds': config.TOKEN_EXPIRATION
        }

    def revoke_all(self, user_id):
        self.token.delete({self.USER_ID: user_id})

    def validate_token(self, token):
        token = self.token.get({self.TOKEN: token})
        if not token:
            raise Error(code=403, message="Invalid token")
        return token.get(self.USER_ID)
