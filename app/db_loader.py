"""
Загружаем в БД ответы пользователю из файлов в папке constants/answers
"""

import logging
import os

from pymongo.errors import DuplicateKeyError

from app.monga_initialize import (
    after_answers_collection,
    answers_collection,
    db,
    disagree_answers_collection,
)

# from app.monga_initialize import connect_to_mongodb

# (
#     db,
#     answers_collection,
#     after_answers_collection,
#     disagree_answers_collection,
# ) = connect_to_mongodb()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s, %(levelname)s, %(message)s",
)
logger = logging.getLogger(__name__)

folders = ["answers", "after_answers", "disagree_answers"]

answers_collection.create_index("key", unique=True)
after_answers_collection.create_index("key", unique=True)
disagree_answers_collection.create_index("key", unique=True)
path = os.path.join("constants")
paths = [os.path.join(path, folder) for folder in folders]


def write_to_db(path, collection):
    for file_name in os.listdir(path):
        with open(
            os.path.join(path, file_name),
            "r",
            encoding="utf-8",
        ) as file:
            answer = " ".join([line.strip() for line in file])
            answer.replace("  ", " ")
            if not answer:
                logger.debug(f"Файл {path}/{file_name} пустой")
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
}

for path in paths:
    db[answers_to_collections.get(path).name].drop()
    write_to_db(path, answers_to_collections.get(path))
