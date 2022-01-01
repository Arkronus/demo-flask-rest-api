from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help='Price has to be specified')
    parser.add_argument('store_id', type=int, required=True,
                        help='Store identifier has to be specified')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        data = Item.parser.parse_args()

        if ItemModel.find_by_name(name):
            return {'message': f'The item with name "{name}" already exists'}, 400

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except Exception as e:
            print(e)
            return {'message': f'An error occurred while inserting item "{name}"'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}, 200

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.store_id = data['store_id']
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
