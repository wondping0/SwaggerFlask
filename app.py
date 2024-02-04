from flask import Flask, jsonify, request
from config import Config
from extensions import mongo
from routes import init_routes
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restx import Api, Namespace
import os
load_dotenv()
import logging

def create_app():
    app = Flask(__name__)
    # Configuration CORS options
    origins = ["http://localhist"]
    allow_headers=["Content-Type", "Authorization"]
    expose_headers=["Content-Type", "Authorization"]
    methods=["GET", "POST", "DELETE"],
    CORS(app, origins=origins, allow_headers=allow_headers, expose_headers=expose_headers, methods=methods)

    # Configure Flask logging
    app.logger.setLevel(logging.INFO)  # Set log level to INFO
    handler = logging.FileHandler('app.log')  # Log to a file
    app.logger.addHandler(handler)

    # import config file
    app.config.from_object(Config)
    
    # initialization moongo database
    mongo.init_app(app)
    
    # initialization jwt token system
    jwt = JWTManager(app)

    # Setting limiter
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["2 per minute", "1 per second"],
    )

    api = Api(app, version='1.0', title='Todo SwaggerFlask API',
        description='A simple Todo SwaggerFlask API',
    )

    ns = Namespace("auth")
        
    # initialization routes
    init_routes(ns, jwt, limiter)
    
    # Adding routes based on swagger
    api.add_namespace(ns)

    @app.errorhandler(500)
    def server_error(error):
        app.logger.exception('An exception occurred during a request.')
        return 'Internal Server Error', 500

    return app
    
if __name__ == '__main__':
    create_app().run(host=os.environ.get('HOST'),port=os.environ.get('PORT'),debug=True)
