import requests


def claim_friend(token, proxy):
    url = "https://gateway.blum.codes/v1/friends/claim"

    payload={}
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
      'Accept-Encoding': 'gzip, deflate, br, zstd',
      'Authorization': f'Bearer {token}',
      'Origin': 'https://telegram.blum.codes',
      'Connection': 'keep-alive',
      'Referer': 'https://telegram.blum.codes/',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-site',
      'Pragma': 'no-cache',
      'Cache-Control': 'no-cache',
      'Content-Length': '0',
      'TE': 'trailers'
    }

    response = requests.request("POST", url, headers=headers, data=payload, proxies=proxy)
    return response
