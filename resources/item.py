from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


# Every Resource has to be a Class
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
	help="Every item needs a store id."
	)


	# HTTP method get item detail
	@jwt_required() # We must be authenticated before calling get method
	def get(self, name):
		item = ItemModel.find_by_name(name)

		if item:
			return item.json()
		#else:
		return {'message': 'Item not found'}


	# HTTP method create
	#@jwt_required() # We must be authenticated before calling post method
	def post(self, name):
		if ItemModel.find_by_name(name): # same as => if Item.find_by_name(name):
			return {'message': "An item with name '{}' already exists.".format(name)}, 400 # Bad request

		# JSON payload
		data = Item.parser.parse_args() # request.get_json()

		item = ItemModel(name, data['price'], data['store_id'])

		try:
			item.save_to_db()
		except:
			return {"message": "An error occurred inserting the item."}, 500 # Internal Server Error

		return item.json(), 201 # Created


	# HTTP method delete
	#@jwt_required() # We must be authenticated before calling delete method
	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()

		return {'message': 'Item deleted'}


	# HTTP method update
	#@jwt_required() # We must be authenticated before calling put method
	def put(self, name):
		# JSON payload
		data = Item.parser.parse_args() # request.get_json()

		item = ItemModel.find_by_name(name)

		if item is None:	# item doesnt exist in db
			item = ItemModel(name, data['price'], data['store_id'])
		else:				# item exists in db
			item.price = data['price']

		item.save_to_db()
		return item.json()



class ItemList(Resource):
	# Method
	def get(self):
		# Using list comprehension
		return {'items': [item.json() for item in ItemModel.query.all()]}

		# or using Lambda function
		#return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}