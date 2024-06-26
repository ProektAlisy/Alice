import pytest
from mongomock import MongoClient

from tests.db_test_operations import (
    delete_data,
    get_data,
    insert_data,
    update_data,
)


@pytest.fixture
def mongo_client():
    client = MongoClient()
    db = client["test_db"]
    yield client
    client.drop_database(db)


def test_insert_document(mongo_client):
    """
    Проверка добавления записи в базу.
    """
    collection = "test_db"
    document = {"name": "Alice", "age": 99}
    result = insert_data(collection, document)
    assert result is not None


def test_get_data(mongo_client):
    """
    Проверка получения записи из базу.
    """
    collection = "test_db"
    query = {"name": "Alice"}
    result = get_data(collection, query)
    assert result is not None


def test_update_data(mongo_client):
    """
    Проверка изменения записи в базе.
    """
    collection = "test_db"
    query = {"name": "Alice"}
    update = {"$set": {"age": 10}}
    result = update_data(collection, query, update)
    assert result is not None
    assert result == 1
    updated_document = get_data(collection, query)
    expected_updated_values = {"name": "Alice", "age": 10}
    assert updated_document == expected_updated_values


def test_delete_data(mongo_client):
    """
    Проверка удаления записи в базе.
    """
    collection = "test_db"
    query = {"name": "Alice"}
    delete_data(collection, query)
    assert get_data(collection, query) is None


def test_get_nonexistent_data(mongo_client):
    """
    Проверка получения несуществующей записи из базы.
    """
    collection = "test_db"
    query = {"name": "Marusia"}
    result = get_data(collection, query)
    assert result is None


def test_delete_nonexistent_data(mongo_client):
    """
    Проверка удаления несуществующей записи из базы.
    """
    collection = "test_db"
    query = {"name": "Maria"}
    result = delete_data(collection, query)
    assert result == 0
    assert get_data(collection, query) is None
