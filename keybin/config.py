from __future__ import absolute_import

import os
from functools import partial

from configparser import ConfigParser


parser = ConfigParser()
path = '{}/../store.cfg'.format(os.path.dirname(os.path.realpath(__file__)))
parser.read(path)
get = partial(parser.get, 'STORE')


HOST = parser.get('APP', 'host')
PORT = parser.getint('APP', 'port')
DEBUG = parser.getboolean('APP', 'debug')

MONGO_HOST = get('host')
MONGO_DB = get('database')
MONGO_STORE_COLLECTION = get('store_collection')
MONGO_USERS_COLLECTION = get('users_collection')
MONGO_TOKEN_COLLECTION = get('token_collection')
TOKEN_EXPIRATION = parser.getint('STORE', 'token_expiration')
