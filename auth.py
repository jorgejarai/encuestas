from __main__ import app
from functools import wraps
from flask import request
import json
from six.moves.urllib.request import urlopen
from functools import wraps
from flask import request, jsonify, _request_ctx_stack
from jose import jwt


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def get_token_auth_header():
    """Obtiene el token de acceso almacenado en la cabecera Authorization"""
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"status": "error",
                         "message":
                         "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"status": "error",
                         "message":
                         "Invalid token format"}, 401)
    elif len(parts) == 1:
        raise AuthError({"status": "error",
                         "message": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"status": "error",
                         "message": "Invalid token format"}, 401)

    token = parts[1]
    return token


def requires_auth(f):
    """Determina si el token de acceso es válido"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen(
            "https://"+app.config["AUTH0_DOMAIN"]+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}

        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }

        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=app.config["ALGORITHMS"],
                    audience=app.config["API_AUDIENCE"],
                    issuer=f"https://{app.config['AUTH0_DOMAIN']}/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"status": "error",
                                 "message": "Token is expired"}, 401)
            except Exception:
                raise AuthError({"status": "error",
                                 "message": "Invalid token format"}, 400)

            _request_ctx_stack.top.current_user = payload

            return f(*args, **kwargs)

        raise AuthError({"status": "error",
                         "message": "Unable to find appropriate key"}, 400)
    return decorated
