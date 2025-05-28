import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("MONGO_DB_FORM")
client = MongoClient(MONGODB_URL)
db = client[DB_NAME]
