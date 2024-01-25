"""
Загружаем в БД ответы пользователю из файлов в папке constants/answers
"""
import logging
import os

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s, %(levelname)s, %(message)s",
)
logger = logging.getLogger(__name__)

client = MongoClient("localhost", 27017)
db = client["dogs_training_center"]

collection = db["answers"]
collection.create_index("key", unique=True)

path = os.path.join("constants", "answers")
for file_name in os.listdir(path):
    with open(os.path.join(path, file_name), "r", encoding="utf-8") as file:
        answer = " ".join([line.strip() for line in file])
        answer.replace("  ", " ")
        if not answer:
            logger.debug(f"Файл {file_name} пустой")
            continue
        try:
            collection.insert_one({"key": file_name[:-4], "answer": answer})
        except DuplicateKeyError:
            logger.debug("Такой ответ уже есть")
