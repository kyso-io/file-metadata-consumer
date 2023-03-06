import os
from dotenv import dotenv_values
from pymongo import MongoClient

config = os.environ["DATABASE_URI"]
print(f"Connecting to database {config}")

if not config:
    raise Exception("DATABASE_URI not found")

client = MongoClient(config)
db = client["kyso"]
