from pymongo import MongoClient
from datetime import datetime, timedelta
import os
import sys
from config import constants
from dotenv import load_dotenv
load_dotenv()


app_configuration = constants.app_config.get(os.getenv("FLASK_ENV"))


def connect_mongo():
    client = MongoClient(app_configuration.MONGO_URI)
    db = client[app_configuration.DB_NAME]
    return db
