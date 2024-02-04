from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt
from extensions import mongo
from models import User, Token
from middleware import create_tokens
from flask_restx import Resource, reqparse, fields
from config import Config
import logging
import yaml

def auth_routes(app, jwt, limiter):
    
    # Router for register
    register_parser = reqparse.RequestParser()
    register_parser.add_argument('username', type=str, required=True, help='Username', location='json')
    register_parser.add_argument('email', type=str, required=True, help='Email', location='json')
    register_parser.add_argument('password', type=str, required=True, help='Password', location='json')
    @app.route('/register')
    class RegisterParameter(Resource):
        @limiter.limit("5 per minute")
        @app.expect(register_parser)
        def post(self):
            data = login_parser.parse_args()
            username = data['username']
            password = data['password']
            email = data['email']

            user = User.create_user(username, email, password)
            if(user):
                return jsonify({'message': 'User registered successfully'})
            else:
                return {'message': 'Error create on same username'}, 400
            
    # Router for login
    login_parser = reqparse.RequestParser()
    login_parser.add_argument('username', type=str, required=True, help='Username', location='json')
    login_parser.add_argument('password', type=str, required=True, help='Password', location='json')
    @app.route('/login')
    class LoginParameter(Resource):
        @limiter.limit("5 per minute")
        @app.expect(login_parser)
        def post(self):
            data = login_parser.parse_args()
            username = data['username']
            password = data['password']
            user = User.get_user_by_username(username=username)
            if user and User.check_password(user, password):
                access_token, refresh_token = create_tokens(identity=str(user['_id']))
                return jsonify(access_token=access_token, refresh_token=refresh_token)
            else:
                return {'error': 'Invalid credentials'}, 400

    # Router for chacking revoke token
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        token = Token.check_token_by_jti(jti)
        return token is not None

    # Router for logout
    logout_parser = reqparse.RequestParser()
    logout_parser.add_argument('Authorization', type=str, help='Bearer <your_access_token>', location='headers')
    @app.route('/logout')
    class LogoutParameter(Resource):
        @limiter.limit("5 per minute")
        @app.expect(logout_parser)
        @jwt_required(verify_type=False)
        def delete(self):
            token = get_jwt()
            jti = token["jti"]
            ttype = token["type"]
            success = Token.revoke_token_by_jti(jti)
            
            if(success):
                return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")
            else: 
                return {"message":"Failed revoke Access token"}, 400

    # Router for refresh token
    refresh_parser = reqparse.RequestParser()
    refresh_parser.add_argument('Authorization', type=str, help='Bearer <your_token>', location='headers')
    @app.route("/refresh")
    class RefreshParameter(Resource):
        @limiter.limit("5 per minute")
        @app.expect(refresh_parser)
        @jwt_required(refresh=True)
        def post(self):
            identity = get_jwt_identity()
            access_token = create_access_token(identity=identity)
            return jsonify(access_token=access_token)

    # Router for checking access
    protected_parser = reqparse.RequestParser()
    protected_parser.add_argument('Authorization', type=str, help='Bearer <your_access_token>', location='headers')
    @app.route('/protected')
    class ProtectedParameter(Resource):
        @limiter.exempt
        @app.expect(protected_parser)
        @jwt_required()
        def get(self):
            current_user_id = get_jwt_identity()
            return jsonify(logged_in_as=current_user_id)
