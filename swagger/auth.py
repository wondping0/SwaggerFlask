from flask_restx import Resource, Namespace

ns = Namespace("auth")

@ns.route('/hello')
class HelloWorldParameter(Resource):
    def post(self,id):
        return 'Hello : '

@ns.route('/login')
class LoginParameters(Resource):
    def post(self,):
        return 'Hello : '