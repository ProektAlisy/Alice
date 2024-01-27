import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_test_host = os.getenv("MONGO_TEST_HOST")
mongo_user = os.getenv("MONGO_TEST_USER")
mongo_pass = os.getenv("MONGO_TEST_PASSWORD")

client = MongoClient(
    host=mongo_test_host,
    username=mongo_user,
    password=mongo_pass,
)
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
