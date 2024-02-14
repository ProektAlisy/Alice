import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_test_host = os.getenv("MONGO_TEST_HOST")
mongo_user = os.getenv("MONGO_TEST_USER")
mongo_pass = os.getenv("MONGO_TEST_PASSWORD")
mongo_port = os.getenv("MONGO_PORT")

uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_test_host}:{mongo_port}/"

client = MongoClient(uri)
db = client["test_db"]


def insert_data(collection, document):
    """
    Функция добавления записи в БД.
    """
    return db[collection].insert_one(document)


def get_data(collection, query):
    """
    Функция получения записи из БД.
    """
    return db[collection].find_one(query, {"_id": 0})


def update_data(collection, query, update_data):
    """
    Функция изменения записи в БД.
    """
    return db[collection].update_one(query, update_data).modified_count


def delete_data(collection, query):
    """
    Функция удаления записи из БД.
    """
    return db[collection].delete_many(query).deleted_count
