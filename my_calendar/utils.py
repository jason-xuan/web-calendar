from functools import wraps
from flask import g, Response
import json


def json_response(d: dict) -> Response:
    return Response(json.dumps(d), mimetype='application/json')


def error_msg(code: int, msg: str) -> Response:
    return json_response({
        'code': code,
        'error': msg
    })


def need_login(func):
    @wraps(func)
    def return_func(*args, **kwargs):
        if g.user is None:
            return error_msg(403, 'need to login')
        return func(*args, **kwargs)
    return return_func




