# My Implementation Swagger and Flask-Python.

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
5. Penggunaan Validasi Input/request
6. Penerapan Data Transfer Objects / AutoMapper
7. Penerapan Rate Limiting