from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)

# We tell SQLAlchemy that our databse is at the root folder of our project.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# Turn off Flask SQLAlchemy modifications tracker, but
# this does NOT turn off the SQLAlchemy modifications tracker.
# So this changes only the extension's behaviors, but not
# the underling SQLAlchemy behavior.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'mirko'
api = Api(app)

# Before first request, SQLAlchemy creates:
# db file and tables unless they exist already.
@app.before_first_request
def create_tables():
    db.create_all()

# JWT creates a new end point: /auth
# When we call /auth => we send username+password.
# JWT extension gets username+password and sends them over authenticate function.
#
# The function authenticate gets username+password to find the correct user
# object using the passed parameter username. Then the function will compare 
# the user object's password with the one received as passed parameter.
# If passwords match, the function authenticate will return the user.
#
# So we got an identity => JWT will return a token.
jwt = JWT(app, authenticate, identity)

# http://127.0.0.1:5000/store/<store-name>
api.add_resource(Store, '/store/<string:name>')	# End point

# http://127.0.0.1:5000/item/<item-name>
api.add_resource(Item, '/item/<string:name>')	# End point

# http://127.0.0.1:5000/items
api.add_resource(ItemList, '/items')			# End point

# http://127.0.0.1:5000/stores
api.add_resource(StoreList, '/stores')			# End point

# http://127.0.0.1:5000/register
api.add_resource(UserRegister, '/register')		# End point

if __name__ == '__main__':
    # Circular import
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)