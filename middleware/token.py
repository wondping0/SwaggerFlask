from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from flask import jsonify
import json

def create_tokens(identity):
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return access_token, refresh_token

def verify_access_token(f):
    @jwt_required()
    @wraps(f)
    def _verify_access_token(*args, **kwargs):
        user_info = {"user":json.loads(get_jwt_identity())}
        # print(user_info)
        kwargs['current_user'] = user_info
        return f(*args, **kwargs)
    return _verify_access_token
