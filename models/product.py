from extensions import mongo
from models.auth import User
from datetime import datetime
from bson import ObjectId

class Product:
    def get_products_collection():
        return mongo.db.products

    def create_product(admin_id, name, price, description):
        products_collection = Product.get_products_collection()
        product_data = {
            'admin_id': admin_id,
            'name': name,
            'price': price,
            'description': description
        }
        product_id = products_collection.insert_one(product_data).inserted_id
        return str(product_id)

    def get_all_products():
        products_collection = Product.get_products_collection()
        return products_collection.find()

    def get_product_by_id(product_id):
        products_collection = Product.get_products_collection()
        return products_collection.find_one({'_id': product_id})

    def buy_product(user_id, product_id):
        users_collection = User.get_users_collection()
        user = users_collection.find_one({'_id': ObjectId(user_id)})

        if not user:
            return "user not found"  # User not found

        products_collection = Product.get_products_collection()
        product = products_collection.find_one({'_id': ObjectId(product_id)})

        if not product:
            return "product not found"  # Product not found

        if 'sold' in product and product['sold']:
            return "Product already sold"

        product_price = product['price']

        # Check if the user has enough balance to buy the product
        if 'balances' not in user or user['balances'] < product_price:
            return "Insufficient balances"

        # Deduct the price from the user's balance
        new_balance = user['balances'] - product_price
        buyed_product_info = []
        if 'buyed_product_info' in user:
            buyed_product_info = user['buyed_product_info']
        new_buyed_product_info = {
            'product_id': product_id,
            'purchase_date': str(datetime.now())
        }
        buyed_product_info.append(new_buyed_product_info)
        users_collection.update_one({'_id': user['_id']}, {'$set': {'balance': new_balance, 'buyed_product_info':buyed_product_info}})

        # Mark the product as sold and record the purchase
        sold_info = {
            'buyer_id': user_id,
            'purchase_date': str(datetime.now())
        }
        products_collection.update_one({'_id': product['_id']}, {'$set': {'sold': True, 'sold_info': sold_info}})

        return "Purchase successful"

    def get_product_purchased_by_user(user_id):
        users_collection = User.get_users_collection()
        user = users_collection.find_one({'_id': ObjectId(user_id)})

        if 'buyed_product_info' not in user:
            return []
        else:
            return user['buyed_product_info']