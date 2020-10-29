import sqlite3
from flask_restful import Resource, reqparse
from Models.user import UserModel


# Resource dos objetos UserRegister
class UserRegister(Resource):
    parser = reqparse.RequestParser()

    # Argumentos aceitos pela API
    parser.add_argument( 'username',
        type=str,
        required=True,
        help="This field cannot be left blank!",
        case_sensitive=True
    )

    parser.add_argument( 'password',
        type=str,
        required=True,
        help="This field cannot be left blank!",
        case_sensitive=True
    )

    # Verificando a existência do usuário
    # Criando usuário no DB, caso não exista
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'Message': 'A user with that username already exists.'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'Message': 'User created successfully.'}, 200