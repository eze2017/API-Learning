
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name =?"
        result = cursor.execute(query,(name,))
        row  = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name' : row[0],'price':row[1]}}
        return {'Message' : 'Item Not Found'} , 404

    def post(self, name):
        #data = Item.parser.parse_args()

        if next(iter(filter(lambda x: x['name'] == name, items)), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item

    @jwt_required()
    def delete(self, name):
        global items
        items = list(iter(filter(lambda x: x['name'] != name, items)))
        return {'message': 'Item deleted'}

    #@jwt_required()
    def put(self, name):
        #data = Item.parser.parse_args()
        data = Item.parser.parse_args()
# Once again, print something not in the args to verify everything works
        item = next(iter(filter(lambda x: x['name'] == name, items)), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item



class ItemList(Resource):
    def get(self):
        return {'items': items}
