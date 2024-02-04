from extensions import mongo

class Token:
    def get_token_collection():
        return mongo.db.tokens

    def revoke_token_by_jti(jti):
        token_collections = Token.get_token_collection()
        token_id = token_collections.insert_one({"jti":jti}).inserted_id
        return str(token_id)

    def check_token_by_jti(jti):
        token_collections = Token.get_token_collection()
        return token_collections.find_one({'jti': jti})
        