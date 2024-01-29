# import os
#
# import pytest
# from mongomock import MongoClient
# from .db_test_operations import insert_data, get_data, update_data, delete_data
# from dotenv import load_dotenv
#
# load_dotenv()
#
# mongo_test_host = os.getenv("MONGO_TEST_HOST")
# mongo_user = os.getenv("MONGO_TEST_USER")
# mongo_pass = os.getenv("MONGO_TEST_PASSWORD")
#
#
# @pytest.fixture
# def mongo_client():
#     client = MongoClient(host=mongo_test_host, username=mongo_user, password=mongo_pass)
#     db = client["test_db"]
#     yield client
#     client.drop_database(db)
#
#
# def test_insert_document(mongo_client):
#     """
#     Проверка добавления записи в базу.
#     """
#     collection = "test_db"
#     document = {"name": "Alice", "age": 99}
#     result = insert_data(collection, document)
#     assert result is not None
#
#
# def test_get_data(mongo_client):
#     """
#     Проверка получения записи из базу.
#     """
#     collection = "test_db"
#     query = {"name": "Alice"}
#     result = get_data(collection, query)
#     assert result is not None
#
#
# def test_update_data(mongo_client):
#     """
#     Проверка изменения записи в базе.
#     """
#     collection = "test_db"
#     query = {"name": "Alice"}
#     update = {"$set": {"age": 10}}
#     result = update_data(collection, query, update)
#     assert result is not None
#     assert result == 1
#     updated_document = get_data(collection, query)
#     expected_updated_values = {"name": "Alice", "age": 10}
#     assert updated_document == expected_updated_values
#
#
# def test_delete_data(mongo_client):
#     """
#     Проверка удаления записи в базе.
#     """
#     collection = "test_db"
#     query = {"name": "Alice"}
#     delete_data(collection, query)
#     assert get_data(collection, query) is None
#
#
# def test_get_nonexistent_data(mongo_client):
#     """
#     Проверка получения несуществующей записи из базы.
#     """
#     collection = "test_db"
#     query = {"name": "Marusia"}
#     result = get_data(collection, query)
#     assert result is None
#
#
# def test_delete_nonexistent_data(mongo_client):
#     """
#     Проверка удаления несуществующей записи из базы.
#     """
#     collection = "test_db"
#     query = {"name": "Maria"}
#     result = delete_data(collection, query)
#     assert result == 0
#     assert get_data(collection, query) is None
