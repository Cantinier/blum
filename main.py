import csv
import json
import threading
import queue
import time
import random

import requests
import logging

import auth_requests


def read_csv():
    with open("accounts.csv", 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        return list(reader)

class TaskQueue:
    def __init__(self):
        self.queue = queue.Queue()

    def add_task(self, task):
        self.queue.put(task)

    def get_task(self):
        return self.queue.get()

    def task_done(self):
        self.queue.task_done()


class WorkerThread(threading.Thread):
    def __init__(self, task_queue, api_client):
        threading.Thread.__init__(self)
        self.task_queue = task_queue
        self.api_client = api_client

    def run(self):
        while True:
            task = self.task_queue.get_task()
            if task is None:
                break
            try:
                self.process_task(task)
            except Exception as e:
                logging.error(f"Error processing task: {e}")
            self.task_queue.task_done()

    def process_task(self, task):
        profile_id = task['profile_id']
        auth_data = task['auth_data']
        proxy = task['proxy']
        self.api_client.play_game(profile_id, auth_data, proxy)


class ThreadManager:
    def __init__(self, num_threads, api_client):
        self.task_queue = TaskQueue()
        self.threads = []
        for _ in range(num_threads):
            thread = WorkerThread(self.task_queue, api_client)
            thread.start()
            self.threads.append(thread)

    def add_task(self, task):
        self.task_queue.add_task(task)

    def wait_completion(self):
        self.task_queue.queue.join()
        for _ in self.threads:
            self.task_queue.add_task(None)
        for thread in self.threads:
            thread.join()


# API клиент
class APIClient:
    def __init__(self):
        self.session = requests.Session()

    def get_balance(self, token, proxy):
        response = self.session.get(
            f"https://game-domain.blum.codes/api/v1/user/balance",
            headers={
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
            },
            proxies={'http': proxy, 'https': proxy}
        )
        response.raise_for_status()
        return response.json()

    def play(self, profile_id, token, proxy):
        response = self.session.post(
            f"https://game-domain.blum.codes/api/v1/game/play",
            headers={
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
            },
            proxies={'http': proxy, 'https': proxy}
        )
        response.raise_for_status()
        game_id = response.json()['gameId']
        print(f'{profile_id} | Стартую игру {game_id}')
        return game_id

    def game_claim(self, token, proxy, game_id):
        points = random.randint(200, 300)
        response = self.session.post(
            url="https://game-domain.blum.codes/api/v1/game/claim",

            json=json.dumps({
                "gameId": f'{game_id}',
                "points": points
            }),
            headers={
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
            },
            proxies={'http': proxy, 'https': proxy}
        )
        return response.text

    def play_game(self, profile_id, auth_data, proxy=None):
        token = auth_requests.get_token(profile_id, auth_data, proxy)
        available_count = self.get_balance(token=token, proxy=proxy)['playPasses']
        if available_count == 0:
            print(f'{profile_id} | Нет повторов')
        else:

            for _ in range(available_count):
                game_id = self.play(profile_id, token, proxy)
                time.sleep(random.randint(30, 33))
                game_result = self.game_claim(token=token, proxy=proxy, game_id=game_id)
                current_balance = self.get_balance(token=token, proxy=proxy)['availableBalance']
                print(profile_id + " | "+game_id + ' ' + game_result + ' | Баланс: ' + current_balance)


def main():
    data = read_csv()
    api_client = APIClient()
    thread_manager = ThreadManager(num_threads=10, api_client=api_client)

    for record in data:
        thread_manager.add_task(record)

    thread_manager.wait_completion()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
