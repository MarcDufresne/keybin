from functools import wraps
from flask import Response


class Error(Exception):

    def __init__(self, code=None, message=None):
        self.code = code or 500
        self.message = message or "Error occurred"


def error_handler(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Error as e:
            return Response(response=e.message, status=e.code)
    return wrapper
