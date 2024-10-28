import random
import requests

from config import X_API_KEY


def create_payload(token, game_id, points, dogs, proxy):
    url = f'https://blum-pro.vercel.app/api/blum/payload'
    payloads = {
        "game_id": f'{game_id}',
        "points": points,
        "dogs": dogs
    }
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': X_API_KEY

    }
    response = requests.request("POST", url, headers=headers, json=payloads, proxies=proxy)
    return response.json()["data"]["payload"]


