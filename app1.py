from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
app = Flask(__name__)

'''@app.route('/')  # 'http://www.google.com/'
def home():
    return "Hello World"

app.run(port=5000)
'''
    ## POST - Used to receive Data
    # Get - Used to Send data bacl quicky

## POST /STORE data : {name:}

# GET /store/<string:name>
# GET /STORE
# POST /store?/<string:name> /item {name:,price:}
#    GET /store/<string:name>/item


stores =  [
{
    'name':'My wonderful Store',
    'items':[{
    'name':'My Item',
    'price':15.99
            }
        ]
    }
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/store',methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
    'name' : request_data['name'],
    'items' :[]
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /STORE
@app.route('/store')
def get_stores():
    return jsonify({'stores':stores})

# GET STORE/<string:name>
@app.route('/store/<string:name>') # http://127.0.0.1:5000/store/store_name
def get_store(name):
    ### Iterate Over stores return matching store names if none return Error Messages
    for store in stores:
        if store ['name'] == name:
            return jsonify(store)
    return jsonify({'message':'Store Not Found'})


# POST /store/<string:name>/item {name:,price:}
@app.route('/store/<string:name>/item',methods=['POST']) # http://127.0.0.1:5000/store/store_name
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] ==name:
            new_item ={
            'name':request_data['name'],
            'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message' :'Store  Not Found'})

@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items':store['items']})
    return jsonify({'message':'Store not Found'})


app.run(port=5000)
