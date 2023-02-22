from dotenv import dotenv_values
from pymongo import MongoClient

config = dotenv_values()

if "DATABASE_URI" not in config:
    raise Exception("DATABASE_URI not found in .env file.")

client = MongoClient(config["DATABASE_URI"])
db = client["kyso"]
