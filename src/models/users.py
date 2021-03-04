import sys
import bcrypt
from config import db_connection
from pymongo.errors import OperationFailure


class User():
    def __init__(self):
        """ initialization"""

    def register_user(self, record):
        db = db_connection.connect_mongo()
        result = db.users.insert_one(record)
        return result

    def hash_password(self, password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    # check if user exist

    def is_user_exist(self, email):
        db = db_connection.connect_mongo()
        result = db.users.find_one({"email": email})
        return result

    def login_user(self, email, password):
        db = db_connection.connect_mongo()
        result = db.users.find_one({"email": email})
        if result:
            stored_password = result["password"]
            if bcrypt.hashpw(password, stored_password) == stored_password:
                return result
        return False

    def get_users(self):
        db = db_connection.connect_mongo()
        return list(db.users.find({}, {"email": 1, "privilege": 1, "userName": 1, "_id": 0}))
