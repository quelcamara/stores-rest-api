from db import db

# Modelo dos objetos StoreModel
class StoreModel(db.Model):
    __tablename__ = 'stores'

    # Colunas da tabela "store" no DB
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    # Propriedade da classe StoreModel que estabelece relação com ItemModel
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    # Transformaçaão de objetos para formato JSON
    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

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