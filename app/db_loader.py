"""
Загружаем в БД ответы пользователю из файлов в папке constants/answers
"""
import os

from pymongo.errors import DuplicateKeyError

from app.logger_initialize import logger
from app.monga_initialize import (
    after_answers_collection,
    another_answers_collection,
    answers_collection,
    db,
    disagree_answers_collection,
)

folders = ["answers", "after_answers", "disagree_answers", "another_answers"]

answers_collection.create_index("key", unique=True)
after_answers_collection.create_index("key", unique=True)
disagree_answers_collection.create_index("key", unique=True)
another_answers_collection.create_index("key", unique=True)

path = os.path.join("constants")
paths = [os.path.join(path, folder) for folder in folders]


def write_to_db(file_path, collection):
    """Запись ответов в БД.

    Запись из файлов в папке constants/.

    Args:
        file_path: Путь до папки с файлами.
        collection: Коллекция в БД.
    """
    for file_name in os.listdir(file_path):
        with open(
            os.path.join(file_path, file_name),
            "r",
            encoding="utf-8",
        ) as file:
            answer = " ".join([line.strip() for line in file])
            answer.replace("  ", " ")
            if not answer:
                logger.debug(f"Файл {file_path}/{file_name} пустой")
                continue
            try:
                collection.insert_one(
                    {"key": file_name[:-4], "answer": answer},
                )
            except DuplicateKeyError:
                logger.debug("Такой ответ уже есть")


answers_to_collections = {
    paths[0]: answers_collection,
    paths[1]: after_answers_collection,
    paths[2]: disagree_answers_collection,
    paths[3]: another_answers_collection,
}

if __name__ == "__main__":
    for path in paths:
        db[answers_to_collections.get(path).name].drop()

    logger.info("Запись ответов в БД завершена")

