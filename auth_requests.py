import requests
import json

auth_query = ""


def get_auth(auth_query, proxy=None):
    url = "https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"

    payload = json.dumps({"query": auth_query})
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'content-type': 'application/json',
        'origin': 'https://telegram.blum.codes',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
    }
    response = requests.post(url, headers=headers, data=payload, proxies=proxy)
    return response.json()


def read_token(profile_id, auth_data, proxy):
    try:
        with open(f'tokens\\token_{profile_id}', 'r', encoding='utf-8') as file:
            token = file.read().strip()
            if token:
                return token
            else:
                return refresh_token(profile_id, auth_data, proxy)
    except FileNotFoundError:
        return refresh_token(profile_id, auth_data, proxy)


def refresh_token(profile_id, auth_data, proxy):
    auth = get_auth(auth_data, proxy)
    token = auth.get('token', {}).get('access')
    if token:
        with open(f'tokens\\token_{profile_id}', 'w', encoding='utf-8') as file:
            file.write(token)
    return token


def check_token(token, proxy):
    url = "https://game-domain.blum.codes/api/v1/user/balance"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'authorization': f'Bearer {token}',
        'origin': 'https://telegram.blum.codes',
        'priority': 'u=1, i',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
    }
    response = requests.get(url, headers=headers, proxies=proxy)
    return response


def get_token(profile_id, auth_data, proxy=None):
    token = read_token(profile_id, auth_data, proxy)
    response = check_token(token, proxy)
    if response.status_code == 401:
        token = refresh_token(profile_id, auth_data, proxy)
    return token

