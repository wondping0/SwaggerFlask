from extensions import mongo
from models.auth import User
from datetime import datetime

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
        user = users_collection.find_one({'_id': user_id})

        if not user:
            return None  # User not found

        products_collection = Product.get_products_collection()
        product = products_collection.find_one({'_id': product_id})

        if not product:
            return None  # Product not found

        if 'sold' in product and product['sold']:
            return "Product already sold"

        product_price = product['price']

        # Check if the user has enough balance to buy the product
        if 'balance' not in user or user['balance'] < product_price:
            return "Insufficient balance"

        # Deduct the price from the user's balance
        new_balance = user['balance'] - product_price
        users_collection.update_one({'_id': user['_id']}, {'$set': {'balance': new_balance}})

        # Mark the product as sold and record the purchase
        sold_info = {
            'buyer_id': user_id,
            'purchase_date': datetime.now()
        }
        products_collection.update_one({'_id': product['_id']}, {'$set': {'sold': True, 'sold_info': sold_info}})

        return "Purchase successful"
