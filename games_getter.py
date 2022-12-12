import requests
import json
from json import JSONDecodeError

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
    all_games = get_free_games()
    upcoming_free = [game for game in all_games
                     if game.get("promotions") and game.get("promotions").get("upcomingPromotionalOffers")]

    return upcoming_free

if __name__ == "__main__":
    free = get_upcoming_free()
    free_json = json.dumps(free)
    print(free_json)

