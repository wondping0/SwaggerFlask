import os
from dotenv import load_dotenv
from datetime import timedelta
load_dotenv()

class tokenConfig:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)