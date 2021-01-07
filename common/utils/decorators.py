from flask import g
from functools import wraps


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if g.user_id:
            return f(*args, **kwargs)
        else:
            return {'message': 'Invalid Token', 'data': None}

    return wrapper
