from werkzeug.security import generate_password_hash, check_password_hash
from extensions import mongo

class User:
    def get_users_collection():
        return mongo.db.users

    def create_user(username, email, password):
        users_collection = User.get_users_collection()
        findedUsername = users_collection.find_one({'username': username})
        if(findedUsername):
            return None
        hashed_password = generate_password_hash(password)
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password
        }
        user_id = users_collection.insert_one(user_data).inserted_id
        return str(user_id)

    def get_user_by_username(username):
        users_collection = User.get_users_collection()
        return users_collection.find_one({'username': username})

    def check_password(user, password):
        hashed_password = user['password']
        return check_password_hash(hashed_password, password)
        
