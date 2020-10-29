from flask_restful import Resource
from Models.store import StoreModel


# Resource dos objetos Store
class Store(Resource):

    # Retorna uma loja buscando por <name>
    # E retorna os itens pertencentes àquela loja
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {'Message': 'Store not found.'}, 404

    # Adiciona um loja ao DB
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'Message': "A store with name '{}' already exists.".format(name)}, 400
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'Message': 'An error occurred while creating the store.'}, 500

        return store.json(), 201

    # Deleta uma loja do DB
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        
        return {'Message': 'Store deleted.'}


# Retorna uma lista com todas as lojas cadastradas no DB
class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}