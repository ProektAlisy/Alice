import os

from dotenv import load_dotenv
from pymongo import MongoClient


def connect_to_mongodb():
    load_dotenv()

    mongo_host = os.getenv("MONGO_TEST_HOST")
    mongo_user = os.getenv("MONGO_TEST_USER")
    mongo_pass = os.getenv("MONGO_TEST_PASSWORD")

    client = MongoClient(
        host=mongo_host,
        username=mongo_user,
        password=mongo_pass,
    )
    db = client["database"]
    answers_collection = db["answers"]
    after_answers_collection = db["after_answers"]
    disagree_answers_collection = db["disagree_answers"]

    return (
        answers_collection,
        after_answers_collection,
        disagree_answers_collection,
    )
