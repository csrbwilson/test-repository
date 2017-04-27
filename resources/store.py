from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from section007.models.storemodel import StoreModel


class Store(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('name',
    #                     type=str,
    #                     required=True,
    #                     help="This field is required!"
    #                     )

    # @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()
        return {'message': 'Store not found.'}, 404


    def post(self, name):

        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists".format(name)}, 400 # 400 => BAD REQUEST

        # Store.parser.parse_args()

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': 'An error ocurred inserting item.'}, 500

        return store.json(), 201 # 201 => CREATED

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}

    # def put(self, name):
    #
    #     data = Store.parser.parse_args()
    #
    #     store = StoreModel.find_by_name(name)
    #
    #     if store is None:
    #         store = StoreModel(name)
    #     else:
    #         store.name = data['name']
    #
    #     store.save_to_db()
    #     return store.json(), 201


class StoreList(Resource):

    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
        # return list(map(lambda x: x.json(), ItemModel.query.all()))