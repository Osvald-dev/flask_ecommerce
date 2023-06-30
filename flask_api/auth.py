from functools import wraps
from flask import abort, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError

def jwt_required():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                verify_jwt_in_request()
                return f(*args, **kwargs)
            except NoAuthorizationError:
                abort(401, 'Token de acceso no proporcionado o inválido')

        return decorated
    return decorator

def admin_required():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                claims = request.jwt_claims
                if not claims.get('is_admin'):
                    abort(403, 'Acceso no autorizado')
                return f(*args, **kwargs)
            except NoAuthorizationError:
                abort(401, 'Token de acceso no proporcionado o inválido')

        return decorated
    return decorator
