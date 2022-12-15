from pymongo import MongoClient
from config import MONGO_CONN_LINK

client = MongoClient(MONGO_CONN_LINK)
db = client.freeEGS_users

def get_user_tz(user_id):
    user = db.users.find_one({"user_id": user_id})
    if user:
        return user.get("timezone")
    return None
