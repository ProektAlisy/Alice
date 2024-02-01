import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


# def connect_to_mongodb():
mongo_host = os.getenv("MONGO_HOST")
mongo_user = os.getenv("MONGO_USER")  # noqa
mongo_pass = os.getenv("MONGO_PASSWORD")  # noqa

client = MongoClient(
    host=mongo_host,
    # username=mongo_user,
    # password=mongo_pass,
)
db = client["database"]
answers_collection = db["answers"]
after_answers_collection = db["after_answers"]
disagree_answers_collection = db["disagree_answers"]
# return (
#     db,
#     answers_collection,
#     after_answers_collection,     disagree_answers_collection,
# )
