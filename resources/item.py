from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs store id."
                        )


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        
        if item:
            return item.json()
        #else: we can skip else, cause if upper will not happen - we will exit the loop anyway 
        return {'message': 'Item does not exist.'}

    def post(self, name):
        # if next(filter(lambda x: x['name'] == name, items), None):
        #     # 400 = bad request code
        #     return {'message': "An item with name '{}' already exists.".format(name)}, 400
        
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
            
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item.'}, 500

        return item.json(), 201  # return code 201 = Created
    
    def delete(self, name):
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {'message': 'Item deleted'}
        
        # to db version
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        
        # query = "DELETE FROM items WHERE name = ?"
        # cursor.execute(query, (name,))
        
        # connection.commit()
        # connection.close()
        # return {'message': 'Item deleted'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            
        return {'message': 'Item deleted'}

    def put(self, name):

        data = Item.parser.parse_args()
        
        

        # tu robię trochę po swojemu, bo wydaje mi się bardziej elegancko
        # item = ItemModel(name, data['price'])
        # version without SQLAlchemy        
        # if ItemModel.find_by_name(name):
        #     try:
        #         item.update()
        #     except:
        #         return {'message':'An error occured updating the item.'}, 500
        # else:
        #     try:
        #         item.insert()
        #     except:
        #         return {'message': 'An error occured inserting the item.'}, 500
        # return item.json()

        #version with SQLAlchemy
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        
        item.save_to_db()
        
        return item.json()
        
        

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]} # using list comperhension
        
        # using lambda function
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        
        # withoit SQLAlchemy
        '''connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
                       
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name':row[1], 'price': row[2]})
           
        connection.close()
        
        return {'items': items}'''
