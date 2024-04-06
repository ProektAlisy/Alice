from mongomock import MongoClient

client = MongoClient()
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
