import requests
import json


def get_free_games() -> dict:
    api_url = (
        'https://store-site-backend-static.ak.epicgames.com/'
        'freeGamesPromotions?locale=ru-RU&country=RU'
    )
    data = requests.get(api_url).json()
    return data


free = get_free_games()
free_json = json.dumps(free)

print(free_json)

