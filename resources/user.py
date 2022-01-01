import sqlite3
from flask_restful import reqparse, Resource
from models.user import UserModel    

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help='Username has to be provided')
    parser.add_argument('password', type=str, required=True,
                        help='Password has to be provided')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User with username ' + data['username'] + ' already registered'}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {'message': 'User created', 'username': data['username']}, 201
