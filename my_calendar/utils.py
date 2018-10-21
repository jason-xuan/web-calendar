from functools import wraps
from flask import g, Response, request
from uuid import uuid4
import json
import re


re_email = re.compile(r"^[0-9A-Za-z\.]*@[A-Za-z\.]*$")
re_word = re.compile(r'^[\w\s]*$')


def check_email(email: str) -> bool:
    return re_email.match(email) is not None


def check_word(word: str) -> bool:
    return re_word.match(word) is not None


def new_uuid():
    return str(uuid4()).replace('-', '')


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


def check_fields(*fields):
    def actual_decorator(func):
        @wraps(func)
        def wrapper_check_fields(*args, **kwargs):
            json_content = request.json
            if json_content is None:
                return error_msg(403, 'post type must be json')
            for (field, field_type) in fields:
                if field not in json_content:
                    return error_msg(403, 'fields not complete')
                if type(json_content[field]) is not field_type:
                    return error_msg(403, f'error type of {field}: expect {field_type} but get {type(field)}')
            return func(*args, **kwargs)
        return wrapper_check_fields
    return actual_decorator
