import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_test_host = os.getenv("MONGO_TEST_HOST")
mongo_user = os.getenv("MONGO_TEST_USER")
mongo_pass = os.getenv("MONGO_TEST_PASSWORD")


def insert_data(collection, document):
    """
    Функция добавления записи в БД.
    """
    client = MongoClient(host=mongo_test_host, username=mongo_user, password=mongo_pass)
    db = client["test_db"]
    return db[collection].insert_one(document)


def get_data(collection, query):
    """
    Функция получения записи из БД.
    """
    client = MongoClient(host=mongo_test_host, username=mongo_user, password=mongo_pass)
    db = client["test_db"]
    res = db[collection].find_one(query, {"_id": 0})
    return res


def update_data(collection, query, update_data):
    """
    Функция изменения записи в БД.
    """
    client = MongoClient(host=mongo_test_host, username=mongo_user, password=mongo_pass)
    db = client["test_db"]
    result = db[collection].update_one(query, update_data)
    return result.modified_count


def delete_data(collection, query):
    """
    Функция удаления записи из БД.
    """
    client = MongoClient(host=mongo_test_host, username=mongo_user, password=mongo_pass)
    db = client["test_db"]
    result = db[collection].delete_many(query)
    return result.deleted_count
