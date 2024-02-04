from routes.auth import auth_routes

def init_routes(app, jwt, limit):
    auth_routes(app, jwt, limit)