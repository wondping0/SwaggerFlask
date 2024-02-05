from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt
from extensions import mongo
from models import User, Token
from middleware import create_tokens, verify_access_token
from middleware import is_valid_email, is_strong_password
from flask_restx import Resource, reqparse, fields
from config import Config
import logging
import yaml
import json

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
            try:
                data = register_parser.parse_args()
                username = data['username']
                password = data['password']
                email = data['email']
                if(not is_valid_email(email)):
                    app.logger.warning("Email Validation Failed to: "+ email)
                    return {'message': 'Email is not valid'}, 400
                if(not is_strong_password(password)):
                    app.logger.warning("Password Validation Failed to: "+ password)
                    return {'message': 'Password is not valid!\n Please user strong password that following this rule:\n- At least 8 characters long\n- Contains at least one uppercase letter\n- Contains at least one lowercase letter\n- Contains at least one digit\n- Contains at least one special character (e.g., !@#$%^&*)\n'}, 400
                user = User.create_user(username, email, password)
                if(user):
                    app.logger.info("Create user "+str(user))
                    return jsonify({'message': 'User registered successfully'})
                else:
                    app.logger.warning("Error create on same username: "+str(user))
                    return {'message': 'Error create on same username'}, 400
            except Exception as e:
                app.logger.error(f"Error on {e}")
                return {'server error':f"Error on {e}"}, 500

    # Router for login
    login_parser = reqparse.RequestParser()
    login_parser.add_argument('username', type=str, required=True, help='Username', location='json')
    login_parser.add_argument('password', type=str, required=True, help='Password', location='json')
    @app.route('/login')
    class LoginParameter(Resource):
        @limiter.limit("5 per minute")
        @app.expect(login_parser)
        def post(self):
            try:
                data = login_parser.parse_args()
                username = data['username']
                password = data['password']
                # if(not is_strong_password(password)):
                #     app.logger.warning("Password Validation Failed to: "+ password)
                #     return {'message': 'Password is not valid!\n Please user strong password that following this rule:\n- At least 8 characters long\n- Contains at least one uppercase letter\n- Contains at least one lowercase letter\n- Contains at least one digit\n- Contains at least one special character (e.g., !@#$%^&*)\n'}, 400
                user = User.get_user_by_username(username=username)
                if user and User.check_password(user, password):
                    app.logger.info(str(user)+"is on login")
                    access_token, refresh_token = create_tokens(identity=json.dumps({'id':str(user['_id']),'is_admin':user['is_admin']}))
                    return jsonify(access_token=access_token, refresh_token=refresh_token)
                else:
                    app.logger.warning(str(user)+"is on invalid credential")
                    return {'error': 'Invalid credentials'}, 400
            except Exception as e:
                app.logger.error(f"Error on {e}")
                return {'server error':f"Error on {e}"}, 500

    # Router for chacking revoke token
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        try:
            jti = jwt_payload["jti"]
            token = Token.check_token_by_jti(jti)
            return token is not None
        except Exception as e:
            app.logger.error(f"Error on {e}")
            return {'server error':f"Error on {e}"}, 500

    # Router for logout
    logout_parser = reqparse.RequestParser()
    logout_parser.add_argument('Authorization', type=str, help='Bearer <your_access_token>', location='headers')
    @app.route('/logout')
    class LogoutParameter(Resource):
        @limiter.limit("5 per minute")
        @app.expect(logout_parser)
        @jwt_required(verify_type=False)
        def delete(self):
            try:
                token = get_jwt()
                jti = token["jti"]
                ttype = token["type"]
                success = Token.revoke_token_by_jti(jti)
                if(success):
                    app.logger.info(str(token)+"is on revoked")
                    return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")
                else: 
                    app.logger.warning(str(token)+"is failed revoke")
                    return {"message":"Failed revoke Access token"}, 400
            except Exception as e:
                app.logger.error(f"Error on {e}")
                return {'server error':f"Error on {e}"}, 500

    # Router for refresh token
    refresh_parser = reqparse.RequestParser()
    refresh_parser.add_argument('Authorization', type=str, help='Bearer <your_token>', location='headers')
    @app.route("/refresh")
    class RefreshParameter(Resource):
        @limiter.limit("5 per minute")
        @app.expect(refresh_parser)
        @jwt_required(refresh=True)
        def post(self):
            try:
                identity = get_jwt_identity()
                app.logger.info("Refresh token on identity: "+str(identity))
                access_token = create_access_token(identity=identity)
                return jsonify(access_token=access_token)
            except Exception as e:
                app.logger.error(f"Error on {e}")
                return {'server error':f"Error on {e}"}, 500

    # Router for checking access
    protected_parser = reqparse.RequestParser()
    protected_parser.add_argument('Authorization', type=str, help='Bearer <your_access_token>', location='headers')
    @app.route('/protected')
    class ProtectedParameter(Resource):
        @limiter.exempt
        @app.expect(protected_parser)
        @verify_access_token
        def get(self, current_user):
            try:
                app.logger.info("Getting access for current_user: "+str(current_user))
                return jsonify(logged_in_as=current_user)
            
            except Exception as e:
                app.logger.error(f"Error on {e}")
                return {'server error':f"Error on {e}"}, 500
