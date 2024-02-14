import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_host = os.getenv("MONGO_TEST_HOST")
mongo_user = os.getenv("MONGO_TEST_USER")
mongo_pass = os.getenv("MONGO_TEST_PASSWORD")
mongo_port = os.getenv("MONGO_PORT")

# uri = ("mongodb://adminUser:adminPassword@"
#        "www.guidedogs.acceleratorpracticum.ru"
#        ":27017/?authSource=adminUser")

client = MongoClient(
    'www.guidedogs.acceleratorpracticum.ru',
    username='adminUser',
    password='adminPassword',
    authMechanism='SCRAM-SHA-256',
)

db = client["database"]
answers_collection = db["answers"]
after_answers_collection = db["after_answers"]
disagree_answers_collection = db["disagree_answers"]
another_answers_collection = db["another_answers"]
