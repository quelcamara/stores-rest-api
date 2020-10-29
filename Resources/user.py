# "Resources" são arquivos de dados
# Que se comunicam com a API
# São as possibilidades de manipulação de determinado dado
# Que os clientes das APIs são capazes de utilizar 
# Essencialmente, "Resources" são o que as APIs pensam
# E como elas se comportam com determinado objeto
# As ações que são permitidas para determinado objeto

import sqlite3
from flask_restful import Resource, reqparse
from Models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
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

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'Message': 'A user with that username already exists.'}, 400

        user = UserModel(**data) # Mesmo que: <data['username], data['password]>
        user.save_to_db()

        return {'Message': 'User created successfully.'}, 200