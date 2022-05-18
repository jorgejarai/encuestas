from __main__ import app
from functools import wraps
from pickle import decode_long
from flask import request, abort
import jwt


def check_token(token):
    """Revisa si un JWT es válido. De serlo, retorna su contenido. En caso
    contrario, retorna None"""

    ret = None

    try:
        ret = jwt.decode(token, app.config["JWT_SECRET"], algorithms="HS256")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

    return ret


def requires_auth(**dec_kwargs):
    role = None
    if 'role' in dec_kwargs:
        role = dec_kwargs['role']

    def decorator(f):
        """Decorador para rutas que requieren autenticación"""
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization').split(' ')[1]
            decoded = check_token(token)

            if not decoded:
                abort(401)

            if role and role != decoded["role"]:
                abort(401)

            return f(*args, **kwargs)

        return wrapper

    return decorator
