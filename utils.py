from aiogram import types
from mongodb_connector import get_user
import datetime as dt
import pytz


def localize_time(from_time_str: str, upto_time_str: str, user_id: int):
    from_stmp = pytz.utc.localize(dt.datetime.strptime(from_time_str, "%Y-%m-%dT%H:%M:%S.%fZ"))
    upto_stmp = pytz.utc.localize(dt.datetime.strptime(upto_time_str, "%Y-%m-%dT%H:%M:%S.%fZ"))
    user = get_user(user_id)
    if user:
        user_tz_offset = user.get('timezone')
        user_tz = dt.timezone(dt.timedelta(hours=user_tz_offset))
        from_stmp = from_stmp.astimezone(user_tz)
        upto_stmp = upto_stmp.astimezone(user_tz)
    return (f"{from_stmp:%d.%m.%Y %H:%M}",
            f"{upto_stmp:%d.%m.%Y %H:%M} ({upto_stmp:%Z})")


def get_timezone_kb():
    buttons = [
        types.InlineKeyboardButton(text='+ 15 мин', callback_data="tz_plus15min"),
        types.InlineKeyboardButton(text='+ 30 мин', callback_data="tz_plus30min"),
        types.InlineKeyboardButton(text='+ 1 ч', callback_data="tz_plus1h"),
        types.InlineKeyboardButton(text='- 15 мин', callback_data="tz_minus15min"),
        types.InlineKeyboardButton(text='- 30 мин', callback_data="tz_minus30min"),
        types.InlineKeyboardButton(text='- 1 ч', callback_data="tz_minus1h"),
        types.InlineKeyboardButton(text='Подтвердить ✅', callback_data='tz_done'),
        types.InlineKeyboardButton(text='Отмена ❌', callback_data='tz_abort')
    ]
    kb = types.InlineKeyboardMarkup(row_width=3)
    kb.add(*buttons)
    return kb


def is_games_same(db_latest: list, current: list):
    if len(db_latest) == len(current):
        ziped = list(zip(db_latest, current))
        return all(cur['title'] == db['title'] for (cur, db) in ziped)
    else:
        return False
