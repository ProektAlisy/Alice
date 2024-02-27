import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_host = os.getenv("ME_CONFIG_MONGODB_URL")
mongo_user = os.getenv("ME_CONFIG_MONGODB_ADMINUSERNAME")
mongo_pass = os.getenv("ME_CONFIG_MONGODB_ADMINPASSWORD")


client = MongoClient(
    mongo_host,
    username=mongo_user,
    password=mongo_pass,
)

db = client["database"]
answers_collection = db["answers"]
after_answers_collection = db["after_answers"]
disagree_answers_collection = db["disagree_answers"]
another_answers_collection = db["another_answers"]
