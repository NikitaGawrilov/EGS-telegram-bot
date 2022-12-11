import requests
import json
from json import JSONDecodeError

locales = {
    "ru": ("ru-RU", "RU"),
    "us": ("en-US", "US")
}

def get_free_games(locale: str = "ru"):
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

    currently_free = [game for game in all_games
                      if game.get("promotions") and game.get("promotions").get("promotionalOffers")]

    upcoming_free = [game for game in all_games
                     if game.get("promotions") and game.get("promotions").get("upcomingPromotionalOffers")]

    return {
        "cur": currently_free,
        "upcome": upcoming_free
    }


free = get_free_games()
free_json = json.dumps(free)

print(free_json)

