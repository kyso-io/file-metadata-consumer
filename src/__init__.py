import os
from dotenv import dotenv_values
from pymongo import MongoClient

config = os.environ["DATABASE_URI"]

if not config:
    raise Exception("DATABASE_URI not found")

client = MongoClient(config["DATABASE_URI"])
db = client["kyso"]
