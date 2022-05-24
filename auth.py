from __main__ import app
from functools import wraps
from flask import request, abort
from db.users import Users
import jwt
import datetime


def generate_token(email: str):
    """Genera un JWT para un email dado."""

    return jwt.encode({
        "sub": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
    }, app.config["JWT_SECRET"], algorithm="HS256")


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
            if not 'token' in request.cookies:
                abort(401)

            token = request.cookies['token']
            decoded = check_token(token)

            if not decoded:
                abort(401)

            if role and role != Users().get_role(decoded["sub"]):
                abort(401)

            return f(*args, **kwargs)

        return wrapper

    return decorator
