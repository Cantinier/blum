import requests
import time
import json


def task_without_validate(token, proxy):

    no_validate_tasks = [
        "f7f85b56-3310-4580-be47-7909203206d7",
        "f83c525c-9844-469b-a104-817814f337e7",
        "e05bb747-7d40-4b69-8b99-0f4a9a9305cf",
        "7b1b11eb-ec1e-4677-96b8-1b590b55dcf1",
        "aace23fe-0938-41ee-a77d-f89bee549928",
        "24dd6940-3529-40a4-89e9-cd806bc42708",
        "f542f997-59c1-498c-8612-c58faf4879ac",
        "90acc5fb-a505-4003-9344-9ec7539d23e1",
        "8e2c1d3b-8a33-4dbc-82e1-685b65173150",
        "dafe118b-2602-43e7-a489-ebe50ca6ed0d",
        "d478fff3-945e-4b30-95c2-3470042027e3",
        "0f3d4955-cf79-4cff-afdf-33de9d38728a",
        "5df6e380-1c64-424c-9d28-10f608332441",
        "fc97db37-53df-4031-9d62-2abaf4842259",
        "58f16842-9e8c-4ff0-bcac-3e9eaf237933",
        "6477d4b1-89b5-4405-9410-f6d880abed38",
        "b8c38802-7bb9-405e-a852-0c17d5c09c9b",
        "f67bc8ee-deff-4d57-ac14-060473b084ab",
        "f473ac7c-1941-4edd-b04b-0580f962e6db",
        "ae435cd3-fab6-4d40-8218-55bc61d6d8c3",
        "15b51a11-a19c-420f-b0ac-c4e9be2f5e07",
        "0f5fb56c-60ab-479c-88b8-ec9e9d2e9281",
        "4bd87033-015a-415c-ab9c-eae720bbfcfe",
        "83b5fa87-bb66-469c-9e79-183936d59958",
        "0e503771-5527-4ec4-a4db-352e6124ab42",
        "5bbd3482-400a-4860-8e47-2bcc42ac9c49",
        "cb22f8ec-cc2f-49cb-8eb9-add09fad3682",
        "34c97e43-3e25-4240-834a-54e34029ca7a",
        "817dbad3-3290-4dc3-aa99-846d5f09d46d",
        "2140351e-b0d2-465e-adab-949d1735dc6e",
        "57761ac3-0745-4cd2-be8b-e4231dfc92b5",
        "a1e11655-152d-4aba-8f2c-30c452331723",
        "94640066-4240-466b-8b7c-663ca525878c",
        "84d1a1bc-a914-44c6-bcc0-593d8cbc476b",
        "f0e4827d-f0a6-431e-a8f9-fa74ced77458",
        "bbdd58fd-aa96-487a-b00f-faec45c545c3",
        "e075353e-78b0-4204-b713-ae8c6860d688",
        "ede0f7f9-1dc2-43ae-8a09-5a8f5834ddae",
        "88ac35ee-8c40-4d0d-b310-23e303ada27d",
        "d92d0461-25c4-452f-9c32-a35511316332",
        "ee08bcdb-c297-459e-90b2-0e0a4be1f2d0",
        "7c479ea4-110b-4bc0-9e15-a769d6170e84",
        "16dbcd76-a9a8-4123-967d-a7a0fcd099e8",
        "c86fa64a-0b63-4deb-84f0-5bfa42c6b47f",
        "85f4eaf3-2200-4adf-8fea-c32362319919"
]

    headers = {'accept': 'application/json, text/plain, */*',
               'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
               'authorization': f'Bearer {token}',
               'content-length': '0',
               'lang': 'en',
               'origin': 'https://telegram.blum.codes',
               'priority': 'u=1, i',
               'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129", "Microsoft Edge WebView2";v="129"',
               'sec-ch-ua-mobile': '?0',
               'sec-ch-ua-platform': '"Windows"',
               'sec-fetch-dest': 'empty',
               'sec-fetch-mode': 'cors',
               'sec-fetch-site': 'same-site',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
}

    for token_task in no_validate_tasks:

        requests_urls = {
            "start": f"https://earn-domain.blum.codes/api/v1/tasks/{token_task}/start",
            "claim": f"https://earn-domain.blum.codes/api/v1/tasks/{token_task}/claim"
        }

        payload = {}

        for name, url in requests_urls.items():
            try:
                print(f'Запрос {name}')
                response = requests.request("POST",
                                            url=url,
                                            headers=headers,
                                            data=payload,
                                            proxies=proxy)
                time.sleep(5)
                print(f'task id: {response.json()["id"]} - {response.json()["status"]} |  Reward={response.json()["reward"]}')

            except Exception as error:
                pass
