
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    TABLE_NAME = 'items'
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        try:
            item = self.find_by_name(name)
            if item:
                return item
        except Exception as e:
            print str(e)
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
        try :
            self.insert(item)
        except Exception as e:
            #print str(e)
            return { "Message": " An error Occured inserting values"} ,500
        
        return item, 201

    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query,(item['name'],item['price']))

        connection.commit()
        connection.close()


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
    
    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE {table} SET price=? WHERE name=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    #@jwt_required()
    def put(self, name):
        #data = Item.parser.parse_args()
        data = Item.parser.parse_args()

        item = self.find_by_name(name)

        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try :
                self.insert(updated_item)
            except Exception as e:
                return {"message" : "An error Occured inserting the Item in the database"},500
        else:
            try:
               self.update(updated_item)
            except Exception :
                return {"message" : "An error Occured inserting the Item in the database"},500

        return updated_item






class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
            
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        
        
        items = []
        for row in result :
            items.append({'name': row[0],'price':row[1]})
            
        connection.close()

        return {'items' : items}

        


'''
@classmethod
def update(cls,item):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
        
    query = "UPDATE items SET price = ? WHERE name =?"
    cursor.execute(query,(item['name'],item['price']))

    connection.commit()
    connection.close()
'''