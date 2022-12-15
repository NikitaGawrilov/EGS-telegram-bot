from aiogram import types, md
from mongodb_connector import get_user_tz
import datetime as dt
import pytz


def localize_time(from_time_str: str, upto_time_str: str, user_id: int):
    from_stmp = pytz.utc.localize(dt.datetime.strptime(from_time_str, "%Y-%m-%dT%H:%M:%S.%fZ"))
    upto_stmp = pytz.utc.localize(dt.datetime.strptime(upto_time_str, "%Y-%m-%dT%H:%M:%S.%fZ"))
    user_tz_offset = get_user_tz(user_id)
    if user_tz_offset:
        user_tz = dt.timezone(dt.timedelta(hours=user_tz_offset))
        from_stmp = from_stmp.astimezone(user_tz)
        upto_stmp = upto_stmp.astimezone(user_tz)
    return (f"{from_stmp:%d.%m.%Y %H:%M %Z}",
            f"{upto_stmp:%d.%m.%Y %H:%M %Z}")