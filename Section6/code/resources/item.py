
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
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
            item = ItemModel.find_by_name(name)
            if item:
                return item.json()
        except Exception as e:
            print (str(e))
        return {'Message' : 'Item Not Found'}, 404

    
    def post(self, name):
        #data = Item.parser.parse_args()

        if ItemModel.find_by_name(name):
            return {'message' : "An Item with Name '{}' already Exists".format(name)} ,400

        data = Item.parser.parse_args()

        item = ItemModel(name,data['price'])
        try :
            item.insert()
        except Exception as e:
            #print str(e)
            print (str(e))
            return { "Message": " An error Occured inserting values"} ,500

        
        return item.json(), 201

    


    @jwt_required()
    def delete(self, name):

        if ItemModel.find_by_name(name):
            
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

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try :
                updated_item.insert()
            except Exception as e:
                print (str(e))
                return {"message" : "An error Occured inserting the Item in the database"},500
        else:
            try:
               updated_item.update()
            except Exception :
                print (str(e))
                return {"message" : "An error Occured inserting the Item in the database"},500

        return updated_item.json()






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

        

