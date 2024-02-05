from flask import jsonify
from flask_restx import Resource, reqparse
from middleware import verify_access_token
from models import Product  # Assuming you have the Product model

def product_routes(app, limiter):
    # Router for creating a new product (admin only)
    create_product_parser = reqparse.RequestParser()
    create_product_parser.add_argument('Authorization', type=str, help='Bearer <your_access_token>', location='headers')
    create_product_parser.add_argument('name', type=str, required=True, help='Product name', location='json')
    create_product_parser.add_argument('price', type=float, required=True, help='Product price', location='json')
    create_product_parser.add_argument('description', type=str, required=True, help='Product description', location='json')

    @app.route('/create')
    class CreateProductResource(Resource):
        @limiter.limit("5 per minute")
        @app.expect(create_product_parser)
        @verify_access_token
        def post(self, current_user):
            try:
                if not current_user['user']['is_admin']:
                    app.logger.warning("user "+str(current_user['user']['id']))
                    return {'message': 'You dont have permission to create product'}, 400
                data = create_product_parser.parse_args()
                admin_id = current_user['user']['id']  # Replace with the actual admin ID
                name = data['name']
                price = data['price']
                description = data['description']
                product_id = Product.create_product(admin_id, name, price, description)
                if product_id:
                    app.logger.info("user "+str(current_user['user']['id'])+" successfully created product: "+str(product_id))
                    return jsonify({'message': 'Product created successfully', 'product_id': product_id})
                else:
                    return {'message': 'Error creating the product'}, 400
            
            except Exception as e:
                app.logger.error(f"Error on {e}")
                return {'server error':f"Error on {e}"}, 500

    # Router for getting all products
    get_all_parser = reqparse.RequestParser()
    get_all_parser.add_argument('Authorization', type=str, help='Bearer <your_access_token>', location='headers')
    @app.route('/getall')
    class GetAllProductsResource(Resource):
        @limiter.exempt
        @app.expect(get_all_parser)
        @verify_access_token
        def get(self, current_user):
            try:
                all_products = Product.get_all_products()
                lisdata = []
                for product in all_products:
                    dataset = {}
                    for key, value in product.items():
                        if(key == '_id'): dataset['id'] = str(value)
                        else: dataset[key] = value
                    lisdata.append(dataset)
                print(lisdata)
                app.logger.info("user "+str(current_user['user']['id'])+" get all products")
                return {'products': lisdata}, 200
            except Exception as e:
                app.logger.error(f"Error on {e}")
                return {'server error':f"Error on {e}"}, 500

    # Router for buying a product (user only)
    buy_product_parser = reqparse.RequestParser()
    buy_product_parser.add_argument('Authorization', type=str, help='Bearer <your_access_token>', location='headers')
    buy_product_parser.add_argument('product_id', type=str, required=True, help='Product ID', location='json')
    @app.route('/buy')
    class BuyProductResource(Resource):
        @limiter.limit("5 per minute")
        @app.expect(buy_product_parser)
        @verify_access_token
        def post(self, current_user):
            try:
                data = buy_product_parser.parse_args()
                user_id = current_user['user']['id']
                product_id = data['product_id']

                result = Product.buy_product(user_id, product_id)
                if result == "Purchase successful":
                    app.logger.info("user "+str(current_user['user']['id'])+" success on buying item")
                    return jsonify({'message': 'Product purchased successfully'})
                else:
                    app.logger.warning("user "+str(current_user['user']['id'])+" failed buying item")
                    return {'message': result}, 400
            except Exception as e:
                app.logger.error(f"Error on {e}")
                return {'server error':f"Error on {e}"}, 500

    purchased_parser = reqparse.RequestParser()
    purchased_parser.add_argument('Authorization', type=str, help='Bearer <your_access_token>', location='headers')
    @app.route('/purchased')
    class PurchasedResource(Resource):
        @limiter.limit("1 per second")
        @app.expect(purchased_parser)
        @verify_access_token
        def get(self, current_user):
            try:
                user_id = current_user['user']['id']

                all_item = Product.get_product_purchased_by_user(user_id)
                lisdata = []
                for product in all_item:
                    dataset = {}
                    for key, value in product.items():
                        if(key == '_id'): dataset['id'] = str(value)
                        else: dataset[key] = value
                    lisdata.append(dataset)
                app.logger.info("user "+str(current_user['user']['id'])+" get purchased products")
                return {'products': lisdata}, 200
            except Exception as e:
                app.logger.error(f"Error on {e}")
                return {'server error':f"Error on {e}"}, 500
