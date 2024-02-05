# My Implementation Swagger and Flask-Python.

- [Requirements](#Requirements)
- [How to run](#How-to-run)
- [Level Question](#Level-Question)
- [Answering Question](#Answering-Question)

## Requirements
1. Python ( *Recommend version 3.12.1* )
2. Python-pip ( *Recommend version 24.0* )
3. MongoDB ( *Recommend version 7.0.5* )

## How to run
1. Installing the python requirement module
```bash
pip install -r requirements.txt
``` 
2. Starting your MongoDB database server. 
3. Configure environments on application by creating file **.env** from **.env.example** file.
```.env
MONGO_URI={YOUR_CONNECTION_STRING}
JWT_SECRET_KEY={YOUR_JWT_KEY}
HOST={DEFAULT_127.0.0.1}
PORT=5000
```
4. Starting the app
```bash
python app.py
```
5. For accessing the apps, you can just visit on **http://{HOST}:{PORT}/**
---
The app create for my task ( **indonesian language** )
## Level Question
Buat web API (data API yang ditampilkan bebas bisa berupa item, produk, data personal dsb.)
1. Menerapkan CORS
2. Logging/monitoring
3. Mengamankan Connection String ke DB
4. OAuth/JWT/PASETO (dengan revoke & refresh token)
5. Validasi Input/request
6. Data Transfer Objects / AutoMapper
7. Rate Limiting

note: terapkan saran-saran tersebut sebanyak-banyak untuk nilai lebih baik

## Answering Question
1. Penerapan CORS

    Cross-origin resource sharing (CORS) adalah fitur keamanan browser yang membatasi permintaan HTTP. Pada aplikasi ini pengaturan CORS menggunakan module flask_cors.
    ```python
    # /app.py line 18
    origins = ["http://localhist"]
    allow_headers=["Content-Type", "Authorization"]
    expose_headers=["Content-Type", "Authorization"]
    methods=["GET", "POST", "DELETE"],
    CORS(app, origins=origins, allow_headers=allow_headers, expose_headers=expose_headers, methods=methods)
    ```
2. Penerapan Logging

    Logging berfungsi sebagai monitor kinerja aplikasi  untuk debugging, dan pemantauan. Dalam aplikasi ini Logging menggunakan modul logging pada python. 
    ```python
    # /app.py line 25
    app.logger.setLevel(logging.INFO)  # Set log level to INFO
    handler = logging.FileHandler('app.log')  # Log to a file
    app.logger.addHandler(handler)
    ```
    Untuk result logger dapat dilihat pada file **app.log**

3. Pengamanan Connection String ke DB

    Untuk connection string akan tersimpan dalam Config yang di import dari file **.env**.
    ```python
    # /config/db.py line 5
    ...
    class dbConfig:
        MONGO_URI = os.environ.get('MONGO_URI')

    # /app.py line 27
    ...
    app.config.from_object(Config)
    ```
    Kemudian melakukan setting keys dan variable pada file **.env**
    ```.env
    MONGO_URI=mongodb://localhost:27017/SwaggerFlask
    ...
    ```
4. Penggunaan refresh token dengan JWT beserta fitur revoke

    Menggunakan module **flask_jwt_extended** untuk penerapan JWT token pada auth
    ```python
    # /middleware/token.py
    from flask_jwt_extended import create_access_token, create_refresh_token
    from flask_jwt_extended import jwt_required, get_jwt_identity
    from functools import wraps
    from flask import jsonify
    import json

    def create_tokens(identity):
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        return access_token, refresh_token

    def verify_access_token(f):
        @jwt_required()
        @wraps(f)
        def _verify_access_token(*args, **kwargs):
            user_info = {"user":json.loads(get_jwt_identity())}
            # print(user_info)
            kwargs['current_user'] = user_info
            return f(*args, **kwargs)
        return _verify_access_token
    ```

    Kemudian untuk revoke akan tersimpan pada database MongoDB, berikut route yang digunakan
    ```python
    # /routes/auth.py line 88
    ...
    @app.route('/logout')
    class LogoutParameter(Resource):
        @limiter.limit("5 per minute")
        @app.expect(logout_parser)
        @jwt_required(verify_type=False)
        def delete(self):
            try:
                token = get_jwt()
                jti = token["jti"]
                ttype = token["type"]
                success = Token.revoke_token_by_jti(jti)
                if(success):
                    app.logger.info(str(token)+"is on revoked")
                    return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")
                else: 
                    app.logger.warning(str(token)+"is failed revoke")
                    return {"message":"Failed revoke Access token"}, 400
            except Exception as e:
                app.logger.error(f"Error on {e}")
                return {'server error':f"Error on {e}"}, 500
    ```

5. Penggunaan Validasi Input/request

    Validator digunakan pada email dan password

    ```python
    # /middleware/validator.py
    ...
    def is_strong_password(password):
        """
        Check if a password is strong according to the following criteria:
        - At least 8 characters long
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one digit
        - Contains at least one special character (e.g., !@#$%^&*)

        :param password: The password to be checked
        :return: True if the password is strong, False otherwise
        """
        # source code function is_strong_password 
        ...
    def is_valid_email(email):
        """
        Check if an email address is valid according to a basic pattern.

        :param email: The email address to be checked
        :return: True if the email is valid, False otherwise
        """
        # source code function is_valid_email 
    ```

6. Penerapan Data Transfer Objects / AutoMapper

    Penerapan DTO digunakan pada folder models yang membuat setiap data menjadi object.
    ```python
    # /models/__init__.py
    from models.auth import User
    from models.token import Token
    from models.product import Product
    ```

7. Penerapan Rate Limiting

    Rate limiting aplikasi menggunakan module **flask_limiter**
    ```python
    # /app.py line 38
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per minute", "1 per second"],
    )
    ...

    # example using limiter
    # /routes/auth.py
    ...
    @app.route('/login')
    class LoginParameter(Resource):
        @limiter.limit("5 per minute")
        @app.expect(login_parser)
        def post(self):
    ...
    # set limit on 5 request per minutes
    ```
