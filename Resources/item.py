from flask_restful import Resource, request, reqparse
from flask_jwt import jwt_required
from Models.item import ItemModel


# Resource dos objetos Item
class Item(Resource):
    parser = reqparse.RequestParser() 

    # Argumentos aceitos pela API
    # Obrigatórios
    parser.add_argument('price', 
        type=float,
        required=True,
        help="This field cannot be left blank!"
        )

    parser.add_argument('store_id', 
        type=int,
        required=True,
        help="Every item needs a store id."
        )

    # Retorna um item buscando por <name>
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name) 
        if item:
            return item.json()

        return {'Message': 'Item not found.'}, 404

    # Adiciona um item ao DB
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

    # Deleta um item do DB
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'Message': 'Item deleted.'}

    # Atualiza um item do DB, caso exista
    # Adiciona um item ao DB, caso não exista
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data) 
        else:
            item.price = data['price']
            item.store_id = data['store_id']
            
        item.save_to_db()

        return item.json()


# Retorna a lista de todos os itens do DB
class ItemList(Resource):
    def get(self):
        return {'item': [item.json() for item in ItemModel.query.all()]}
