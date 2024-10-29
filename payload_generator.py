import random
import requests

from config import X_API_KEY


def create_payload(token, game_id, points, dogs, proxy):
    url = f'http://14.225.212.202/api/blum/payload'
    payloads = {
        "game_id": f'{game_id}',
        "points": f'{points}',
        "dogs": f'{dogs}'
    }
    headers = {
          'accept': 'application/json, text/plain, */*',
          'content-type': 'application/json',
          'X-API-KEY': X_API_KEY

    }
    response = requests.request("POST", url, headers=headers, json=payloads, proxies=proxy)
    return response.json()["data"]["payload"]


