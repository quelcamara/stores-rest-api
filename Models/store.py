# Iniciamos esse modelo copiando o modelo item.py
# Depois modificamos para o propósito de "stores", em vez de "items"

from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # Podemos fazer, também, uma referência reversa
    # Configuramos os itens para ter uma propriedade "store"
    # Associada a eles para que pudéssemos identificar
    # A qual loja cada item pertence
    # Podemos também determinar uma referência
    # Que irá permitir que a loja veja quais itens
    # Do banco de dados possuem o "store_id" compatível
    # Com seu próprio "id". E então determinar quais itens
    # Estão cadastrados naquela determinada loja

    # A forma de fazer isso é criando uma propriedade "item"
    # Para cada loja cadastrada, que será capaz de buscar
    # Pela relação existente entre a StoreModel e o ItemModel
    # Assim, quando "items" aqui for criada, ele buscará em ItemModel
    # Qual a relação entre eles e encontrará a "store_id"
    # StoreModel entenderá que poderão existir vários ItemModel
    # Compatíveis com seu "id" e, então, fará com que "items" aqui
    # Seja uma lista de itens que compartilhem seu "id"

    # Toda vez que criarmos uma StoreModel
    # Será criado também um objeto para cada item
    # No banco de dados que seja compatível com aquela StoreModel "id"
    # Se tivermos alguns poucos itens, não haverá problema
    # Mas se tivermos muitos itens, poderá se tornar uma operação muito custosa
    # Então o que podemos fazer é dizer ao SQLAlchemy para não fazer isso
    # Para que ele não vá até a tabela "items" e crie um objeto para cada item
    # A forma de fazermos isso é com lazy=dynamic
    # O que acontecerá:
    # self.items não será mais uma lista de items
    # Ele será agora um "query builder" que terá a habilidade
    # De olhar dentro da tabela "items"
    # Assim, poderemos utilizar self.items.all()
    # Para retornar todos os objetos daquela tabela
    # O que significa que, até que chamemos o método json()
    # Não olharemos dentro da tabela
    # O que significa que criar uma StoreModel não será mais custoso
    # Mas toda vez que acessarmos o método json(), a tabela será vasculhada
    # O que também pode ser lento
    # Será preciso, portanto, optar onde queremos o melhor rendimento
    # Na criação da StoreModel, ou na busca de itens

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name
    
    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()