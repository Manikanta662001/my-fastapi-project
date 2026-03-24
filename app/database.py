from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URL"))
db = client["fastapi_db"]
users_collection = db["users"]
posts_collection = db["posts"]
blacklist_collection = db["blacklist"]