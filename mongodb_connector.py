from pymongo import MongoClient, DESCENDING
from config import MONGO_CONN_LINK
from aiogram import types
from datetime import datetime as dt

client = MongoClient(MONGO_CONN_LINK)
db = client.freeEGS_users


def get_user(user_id):
    user = db.users.find_one({"user_id": user_id})
    if user:
        return user
    return None


def get_all_users():
    users = db.users.find()
    return list(users)


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


def get_latest_giveaway():
    latest = db.currentGiveaway.find().sort('timestamp', DESCENDING)[0]
    latest.pop('_id')
    latest.pop('timestamp')
    return list(latest.values())


def add_current_giveaway(games: list):
    ziped_games = dict(zip(map(str, range(len(games)+1)), games))
    ziped_games.update({'timestamp': dt.utcnow()})
    try:
        db.currentGiveaway.insert_one(ziped_games)
        return True
    except Exception:
        return False
