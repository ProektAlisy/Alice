import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


mongo_test_host = os.getenv("ME_CONFIG_MONGODB_URL")
mongo_user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
mongo_pass = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

client = MongoClient(host=mongo_test_host)
db = client["database"]
answers_collection = db["answers"]
after_answers_collection = db["after_answers"]
disagree_answers_collection = db["disagree_answers"]
another_answers_collection = db["another_answers"]
