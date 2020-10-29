# Criando um modelo para "items"
# Será uma representação de o que um "item" é
# E como ele deveria se parecer
# Os métodos que transferimos para o ItemModel
# São aqueles que não são chamados pela API diretamente
# Eles são utilizados apenas dentro do código
# Para realizar funções internas dos objetos "items"
# Por esse motivo, não faz sentido mantê-los nas "resources"
# Pois isso apenas poluiria o arquivo com código
# Que não faz parte daquela lógica de construção
# Os métodos aqui presentes não modificam a API diretamente
# Mas podem afetar e modificar a forma como o código FUNCIONA

from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2)) # precision=2 <casas decimais>

    # Adicionamos essa coluna na tabela "items"
    # Quando associamos uma "foreign key", conseguimos interligar tabelas através de "rows"
    # Isso se dá ao fato de que teremos diferentes objetos que compartilham valores
    # Dessa forma, podemos associar, por exemplo, itens a uma determinada loja
    # E realizar buscas de itens por lojas ou vice-versa
    # Isso nos permite ter mais controle e segurança de dados, além de flexibilidade
    # Isso porque, não somos capazes de deletar uma "referência" <tabela store>
    # Sem antes deletar as "foreign keys" que a tem como referência
    # Precisaríamos, primeiro, deletar os itens, ou mudar o store_id para deletar a "store"
    # Portanto, uma "Foreign Key" nos permite interligar tabelas

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    # Há uma forma de fazer isso com SQL através de "joins"
    # Mas não precisaremos utilizar essa função join()
    # Pois SQLAlchemy é capaz de fazer isso para nós
    # Tudo que precisamos fazer é "mostrar" que existe um store_id
    # E, então, poderemos encontrar uma store no BD
    # Que seja compatível com a "store_id" 

    # Então, agora, cada ItemModel terá uma propriedade "store"
    # Que será a "store" compatível com a "store_id"
    
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    # Criando um método json() apenas para
    # Retornar uma representação JSON do modelo

    def json(self):
        return {'name': self.name, 'price': self.price}

    # Faz sentido manter esse método como uma @classmethod
    # Porque ele irá retornar um objeto do tipo ItemModel 
    # db do SQLAlchemy já nos retornará um objeto ItemModel
    # Não precisamos especificar a conexão ou cursor
    # Porque SQLAlchemy já faz isso automaticamente

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # Mesmo que <SELECT * FROM Items WHERE name=name LIMIT 1>. Retorna a primeira linha apenas

    # Estas classes não precisam mais ser uma @classmethod
    # Pois o objeto trabalhará com seus próprios atributos
    # Então podemos transformá-los em instance methods <self>
    # E utilizar os atributos para as interações desejadas

    # SQLAlchemy já traduz objetos diretamente para "rows"
    # Então não precisamos dizer que "data row" ele deve inserir
    # Apenas precisamos dizer que ele precisa adicionar determinado objeto
    # "session" é uma coleção de objetos que iremos escrever no BD
    # Podemos adicionar vários objetos nas seções
    # E depois escrevê-los todos de uma vez, o que é mais eficiente
    # Mas, neste caso, como estamos adicionando apemas 01 objeto
    # Iremos apenas adicionar e salvar logo em seguida
    # Este método agora poderá salvar ou atualizar um objeto do DB
    # Isso porque, quando criamos o objeto, ele ganah um ID
    # E ao mudarmos um atributo dele, o SQLAlchemy automaticamente
    # Reconhece se for o mesmo ID que estamos modificando
    # E atualiza os dados informados

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()