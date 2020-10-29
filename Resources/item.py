# Olhando para as "resources", buscamos o que não
# Lhes pertence e transferimos para o ItemModel
# As "resources" são utilizadas para mapear endpoints
# Mas temos alguns outros métodos aqui
# Que não têm a finalidade de mapear endpoints
# São métodos auxiliares da construção dos endopints
# Por esse motivo, eles devem pertencer à representação INTERNA
# Da classe de itens <ao MODELO>
# Os métodos que devem permanecer nas "resources"
# São aqueles que sabemos que, se modificarmos
# Modificaremos o comportamento da API diretamente
# Como os métodos <get, post, delete, put>

from flask_restful import Resource, request, reqparse
from flask_jwt import jwt_required
from Models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser() 
    parser.add_argument('price', 
        type=float,
        required=True,
        help="This field cannot be left blank!"
        )
    # Toda vez que criarmos um ItemModel
    # Teremos que passar uma store_id como parâmetro     
    parser.add_argument('store_id', 
        type=int,
        required=True,
        help="Every item needs a store id."
        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name) # Agora, "item" é um objeto ItemModel
        if item:
            return item.json()

        return {'Message': 'Item not found.'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'Message': "An item with name '{}' already exists.".format(name)}, 400
        
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'Message': 'An error ocurred inserting the item.'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'Message': 'Item deleted.'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data) # Mesmo que: <data['price'], data['store_id']>
        else:
            item.price = data['price']
            item.store_id = data['store_id']
            
        item.save_to_db()

        return item.json()

# Iteramos por toda a lista de itens com uma list comprehension
# E retornamos cada item, individualmente, em formato JSON
# Isso retornará uma lista de itens em formato JSON como "valor" da "chave" "items".

class ItemList(Resource):
    def get(self):
        return {'item': [item.json() for item in ItemModel.query.all()]}
