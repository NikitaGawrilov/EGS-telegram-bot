import requests
import json
from json import JSONDecodeError
import datetime as dt
import pytz

locales = {
    "ru": ("ru-RU", "RU"),
    "us": ("en-US", "US")
}

def get_free_games(locale: str = "ru"): #TODO Переписать всё под aiohttp?
    try:
        api_url = (
            f'https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?'
            f'locale={locales[locale][0]}&'
            f'country={locales[locale][1]}'
        )
    except KeyError:
        raise Exception("Incorrect locale given")

    try:
        raw_data = requests.get(api_url).json()
    except JSONDecodeError:
        raise Exception("Seems like there are some problems with getting or decoding response from EGS servers")

    all_games = raw_data.get("data").get("Catalog").get("searchStore").get("elements")
    if not all_games:
        raise Exception("No games returned by EGS server")

    return all_games

def get_curr_free():
    all_games = get_free_games()
    currently_free = [game for game in all_games
                      if game.get("promotions") and game.get("promotions").get("promotionalOffers")]

    return currently_free

def get_upcoming_free():
    #TODO фильтровать попадания левых игр по акции
    all_games = get_free_games()
    upcoming_free = [game for game in all_games
                     if game.get("promotions")
                     and game.get("promotions").get("upcomingPromotionalOffers")
                     and game.get("promotions").get("upcomingPromotionalOffers")[0]['promotionalOffers'][0]['discountSetting']['discountPercentage'] == 0]

    return upcoming_free


if __name__ == "__main__":
    free = get_free_games()
    free_json = json.dumps(free)
    print(free_json)
    # free = get_upcoming_free()
    # time = free[0]['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers'][0]['startDate']
    # stmp = dt.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    # utc_stmp = pytz.utc.localize(stmp)
    # offset = 5
    # tiz = dt.timezone(dt.timedelta(hours=offset))
    # tz_stmp = utc_stmp.astimezone(tiz)
    # print(time)
    # print(stmp)
    # print(tz_stmp)
    # free_json = json.dumps(free)
    # print(free_json)

