from db import db

# Modelo dos objetos ItemModel
class ItemModel(db.Model):
    __tablename__ = 'items'

    # Colunas da tabela "items" no DB
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # Criação de join entre tabelas
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    
    # Propriedade da classe ItemModel que estabelece relação com StoreModel
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    # Transformaçaão de objetos para formato JSON
    def json(self):
        return {'name': self.name, 'price': self.price}

    # Buscando objetos no DB com nome dado em parâmetro
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    # Salvando objetos no DB 
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Deletando objetos do DB
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()