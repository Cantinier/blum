import requests

from auth_requests import get_token


def claim_rewards_get(token, proxy):
    url = "https://game-domain.blum.codes/api/v1/daily-reward?offset=-180"

    payload={}
    headers = {
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
      'authorization': f'Bearer {token}',
      'origin': 'https://telegram.blum.codes',
      'priority': 'u=1, i',
      'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

    response = requests.request("GET", url, headers=headers, data=payload, proxies=proxy)
    print(response.text)
    return response.text


def claim_rewards_post(token, proxy):

    url = "https://game-domain.blum.codes/api/v1/daily-reward?offset=-1800000"

    payload={}
    headers = {
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
      'authorization': f'Bearer {token}',
      'content-length': '0',
      'origin': 'https://telegram.blum.codes',
      'priority': 'u=1, i',
      'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxy)

    print(response.text)
    return response.text

