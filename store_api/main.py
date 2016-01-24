from __future__ import absolute_import

from flask import Flask, jsonify

from store_api import config
from store_api.database.store import Store
from store_api.database.users import User
from store_api.database.token import Token
from store_api.errors import error_handler
from store_api.utils import json_param


app = Flask(__name__)

user_model = None
store_model = None
token_model = None


@app.route('/register', methods=['POST'])
@error_handler
@json_param('username')
@json_param('password')
def register(username, password):
    user_model.register(username, password)
    return jsonify(result="ok")


@app.route('/unregister', methods=['DELETE'])
@error_handler
@json_param('username')
@json_param('password')
def unregister(username, password):
    user_id = user_model.get(username, password).get(User.USER_ID)
    user_model.unregister(user_id)
    store_model.delete_all(user_id)
    token_model.revoke_all(user_id)
    return jsonify(result='ok')


@app.route('/token', methods=['POST'])
@error_handler
@json_param('username')
@json_param('password')
@json_param('client_id', required=False)
def generate_token(username, password, client_id):
    user_id = user_model.get(username, password).get(User.USER_ID)
    token = token_model.generate(user_id, client_id=client_id)
    return jsonify(token=token)


@app.route('/user/<token>/keys', methods=['GET'])
@error_handler
def get_keys(token):
    user_id = token_model.validate_token(token)
    return jsonify(keys=store_model.get_all_keys(user_id))


@app.route('/user/<token>/store/<key>', methods=['GET'])
@error_handler
def get_stored_data(token, key):
    user_id = token_model.validate_token(token)
    return jsonify(value=store_model.get(key, user_id))


@app.route('/user/<token>/store/<key>', methods=['POST'])
@error_handler
@json_param('value')
def store_data(key, value, token):
    user_id = token_model.validate_token(token)
    store_model.set(key, value, user_id)
    return jsonify(result="ok")


if __name__ == "__main__":
    user_model = User()
    token_model = Token()
    store_model = Store()
    app.run(port=config.PORT, debug=config.DEBUG)
