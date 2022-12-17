from pymongo import MongoClient
from config import MONGO_CONN_LINK
from aiogram import types
import asyncio

client = MongoClient(MONGO_CONN_LINK)
db = client.freeEGS_users

def get_user(user_id):
    user = db.users.find_one({"user_id": user_id})
    if user:
        return user
    return None

def add_user(user: types.User, pics: dict):
    try:
        db.users.insert_one(
            {
                "user_id": user.id,
                "timezone": 0,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "language": user.locale.language,
                "profile_pics": pics
            }
        )
        return True
    except Exception as e:
        print(e)
        return False