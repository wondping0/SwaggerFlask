import os
from dotenv import load_dotenv
load_dotenv()

class dbConfig:
    MONGO_URI = os.environ.get('MONGO_URI')
