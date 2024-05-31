import requests

def check(proxy, exp_ip):
    url = "https://api.myip.com/"

    payload = {}
    headers = {}
    response = requests.get(url, headers=headers, data=payload, proxies=proxy)
    actual_ip = response.json()["ip"]
    status = (exp_ip == actual_ip)
    return status

