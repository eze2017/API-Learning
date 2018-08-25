import sqlite3
from flask_restful import Resource,reqparse
class User:

    def __init__(self,_id,username,password):
        self.id = _id
        self.username =username
        self.password =password

    @classmethod
    def find_by_username(cls,username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()


        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query,(username,))
        row = result.fetchone()
        if row :
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls,_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users where id=?"
        result = cursor.execute(query,(_id,))
        row = result.fetchone()
        if row :
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user


class UserRegister(Resource):
    TABLE_NAME = 'users'

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message" :"A user with that User Name already Exists !"} ,400
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL ,?,?)"
        cursor.execute(query,(data['username'],data['password']))
        connection.commit()
        connection.close()
        return {"Message":"User Created Succesfully"},201


'''
class Unregister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    
    def delete(self):
        
        data = Unregister.parser.parse_args()

        try:
            if User.find_by_username(data['username']):
                connection = sqlite3.connect('data.db')
                cursor  = connection.cursor()
                query = "DELETE FROM users WHERE username = ?"
                cursor.execute(query,(data['username']))
                connection.commit()
                connection.close()
                return {'Message' :  "User Deleted Succesfully"},201
            else:
                return {"Message" : "User does Not Exist with that Username"} , 404
        except:

            return {"Message" : " An Error has Occured "} ,500
            '''