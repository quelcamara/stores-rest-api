# A classe "User" não é um resource porque a API
# Não é capaz de interagir com ela de nenhuma forma
# A API não consegue receber dados desta classe
# Nem enviar dados desta classe em forma de JSON
# Ou coisas do tipo
# Esta classe é, essencialmente, uma "ajudante"
# Que contém alguns dados sobre o usuário
# E que contém alguns métodos que nos permite
# Ter acesso aos usuários <objetos> de um banco de dados
# Ele nos permite ter mais flexibilidade no programa
# Sem poluir o arquivo que contém as resources
# Que irão conter apenas as informações sobre
# As formas como os clientes podem interagir com o programa

# Um MODELO é a representação INTERNA de uma entidade
# Enquanto uma RESOURCE é a represetação EXTERNA de uma entidade

import sqlite3
from db import db

# Quando fazemos dessas classes uma extensão de db.Model
# Estamos dizendo ao SQLAlchemy que essas classes
# São objetos que nós iremos salvar em um BD
# E também serão objetos que iremos ter acesso através do BD
# Precisamos dizer, também, ao SQLAlchemy o nome da tabela
# Onde esses Models vão ser armazenados

class UserModel(db.Model):
    __tablename__ = 'users'

    # Informamos as colunas que queremos que a tabela contenha
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first() # SQLAlchemy converte a linha encontrada em um objeto UserModel 

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
