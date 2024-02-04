from flask_jwt_extended import create_access_token, create_refresh_token

def create_tokens(identity):
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return access_token, refresh_token