import sqlite3
from db import db

# Modelo dos objetos ItemModel
class UserModel(db.Model):
    __tablename__ = 'users'

    # Colunas da tabela "users" no DB
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    # Salvando objetos no DB
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Buscando objetos no DB com username dado em parâmetro
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first() # SQLAlchemy converte a linha encontrada em um objeto UserModel 

    # Buscando objetos no DB com _id dado em parâmetro
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
