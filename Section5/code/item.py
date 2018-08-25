
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
        item = self.find_by_name(name)
        if item:
            return item
        
        return {'Message' : 'Item Not Found'}, 404

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name =?"
        result = cursor.execute(query,(name,))
        row  = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        #data = Item.parser.parse_args()

        if self.find_by_name(name):
            return {'message' : "An Item with Name '{}' already Exists".format(name)} ,400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query,(item['name'],item['price']))

        connection.commit()
        connection.close()

        return item, 201

    @jwt_required()
    def delete(self, name):

        if self.find_by_name(name):
            
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            #data = Item.parser.parse_args()
            
            query = "DELETE FROM items WHERE name = ?"
            cursor.execute(query,(name,))

            connection.commit()
            connection.close()

            return {"Message" : "Item Deleted Succesfully"}
        else:

            return {"Message" : "Item Not Found To Delete"} ,404



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
