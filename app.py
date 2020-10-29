from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

from security import authenticate, identity
from Resources.user import UserRegister
from Resources.item import Item, ItemList
from Resources.store import Store, StoreList

app = Flask(__name__)

# Precisamos dizer ao SQLAlchemy onde encontrar
# O nosso arquivo data.db
# Indicamos aqui que o SQLAlchemy database estará localizado
# Na pasta raíz do nosso projeto
# SQLAlchemy funcionaria com qualquer tipo de BD criado
# Não apenas em um DB do sqlite
# Poderia ser MySQL, PostgreeSQL, Oracle, ou qualquer outro

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# Desabilitamos o rastreador de modificações do Flask-SQLAlchemy
# Porque o SQLAlchemy tem seu próprio rastreador de modificações
# O que é ainda melhor

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

# SQLAlchemy é capaz de criar uma tabela por conta própria
# Não precisamos mais fazer isso manualmente
# Nem ter um código apenas para criar a tabela antes da execução
# Para precisamos dizer ao SQLAlchemy qual será o conteúdo da tabela
# Ele criará o arquivo data.db de início
# Mas não criará nenhuma tabela no arquivo se não indicarmos
# Para isso, usamos o Decorator do Flask @app.before_first_request
# Esse método será executado antes do primeiro "request" deste app
# Quando for executádo, este método criará o arquivo data.db
# E também todo o conteúdo das tabelas "users" e "items"
# A menos que elas já existam no banco de dados

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
