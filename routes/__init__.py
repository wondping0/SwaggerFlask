from routes.auth import auth_routes
from routes.product import product_routes
from flask_restx import Api, Namespace

def init_routes(app, jwt, limit):
    ns_auth = Namespace("auth")
    auth_routes(ns_auth, jwt, limit)
    ns_product = Namespace("product")
    product_routes(ns_product, limit)

    # Adding routes based on swagger
    app.add_namespace(ns_auth)
    app.add_namespace(ns_product)
