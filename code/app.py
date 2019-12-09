from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app,authenticate,identity) # create new endpoint /auth

items = []

class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None) # next give us the first item matched 
        return {'item': item} , 200 if item else 404

    def post(self,name):
        #Error control if user add a name that already exists
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = request.get_json() #force = True to transform content type to json, silent = True it doesnt give an error return none
        item = {'name': name, 'price':data["price"]}
        items.append(item)
        return item, 201
    
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items)) # we overwrite the list without the element deleted
        return {'message': 'Item deleted'}


class ItemList(Resource):
    def get(self):
        return {'items':items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(debug=True, port=5000)

