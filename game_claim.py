import random
import requests


def game_claim_points(token, proxy, game_id):
    points = random.randint(180, 250)

    url = "https://game-domain.blum.codes/api/v1/game/claim"
    payloads = {
        "gameId": f'{game_id}',
        "points": points
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
        'Origin': 'https://telegram.blum.codes',
        'Connection': 'keep-alive',
        'Referer': 'https://telegram.blum.codes/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'trailers'
    }
    response = requests.request("POST", url, headers=headers, json=payloads, proxies=proxy)
    return response.text


