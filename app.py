import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL_2', 'sqlite:///data.db') #first db is default, but if it's not provided (we run app locally) the second (local) db will be used
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turns off Flask SQLAlchemy modifications tracker, but does not turn of SQL Alchemy mod tracker
app.secret_key = 'tomek'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # creates endpoint /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')




if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
