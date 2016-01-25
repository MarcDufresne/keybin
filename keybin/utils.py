from functools import wraps

from flask import request

from keybin.errors import Error


class JsonParam:
    def __init__(self, param_name, required=True):
        self.param_name = param_name
        self.required = required

    def __call__(self, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            json = request.get_json()
            if not json:
                raise Error(
                    code=400,
                    message="Request body is not JSON or is empty"
                )
            param = json.get(self.param_name)
            if self.required and not param:
                raise Error(
                    code=400,
                    message="Required parameter '{}' is missing".format(self.param_name)
                )
            kwargs[self.param_name] = param
            return function(*args, **kwargs)
        return wrapper

json_param = JsonParam
