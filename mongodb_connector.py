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
    if not db.users.find_one({"user_id": user.id}):
        try:
            db.users.insert_one(
                {
                    "user_id": user.id,
                    "timezone": 0,
                    "notify_every_time": True,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "language": user.locale.language,
                    "profile_pics": pics
                }
            )
            return True
        except Exception:
            return False
    else:
        return False

def update_timezone(user_id: int, timezone: int):
    if db.users.find_one({"user_id": user_id}):
        try:
            db.users.update_one(
                {"user_id": user_id},
                {"$set": {"timezone": timezone}}
            )
            return True
        except Exception:
            return False
    else:
        return False