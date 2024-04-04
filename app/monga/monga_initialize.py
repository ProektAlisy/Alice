from pymongo import MongoClient

from app.settings import settings

client = MongoClient(
    host=settings.ME_CONFIG_MONGODB_URL,
    username=settings.ME_CONFIG_MONGODB_ADMINUSERNAME,
    password=settings.ME_CONFIG_MONGODB_ADMINPASSWORD,
)

db = client["database"]
answers_collection = db["answers"]
after_answers_collection = db["after_answers"]
disagree_answers_collection = db["disagree_answers"]
another_answers_collection = db["another_answers"]
