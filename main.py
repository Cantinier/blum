import csv
import json
import threading
import queue
import time
import random
from datetime import datetime

import requests
import logging

import check_proxy
import friend_claim
import game_claim

import auth_requests
import ClaimRewards
import farming

from enum import Enum


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
        self.task_type = 'all'

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
        proxy_data = task['proxy']
        exp_ip = task['proxy_ip']
        if proxy_data != '':
            proxy = {
                "http": f'http://{proxy_data}',
                "https": f'http://{proxy_data}'
            }
            proxy_status = check_proxy.check(proxy, exp_ip)
            if not proxy_status:
                print(profile_id + " | Не пройдена проверка прокси")
            else:
                self.start_task(profile_id, auth_data, proxy)
        else:
            self.start_task(profile_id, auth_data, None)

    def start_task(self, profile_id, auth_data, proxy):
        if self.task_type == 'game':
            self.api_client.play_game(profile_id, auth_data, proxy)
        if self.task_type == 'daily':
            self.api_client.daily(profile_id, auth_data, proxy)
        if self.task_type == 'farming':
            self.api_client.farming(profile_id, auth_data, proxy)
        if self.task_type == 'friend':
            self.api_client.friend_claim(profile_id, auth_data, proxy)
        if self.task_type == 'all':
            self.api_client.farming(profile_id, auth_data, proxy)
            self.api_client.friend_claim(profile_id, auth_data, proxy)
            self.api_client.daily(profile_id, auth_data, proxy)
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
            proxies=proxy
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
            proxies=proxy
        )
        response.raise_for_status()
        game_id = response.json()['gameId']
        print(f'{profile_id}-game | Стартую игру {game_id}')
        return game_id

    def game_claim(self, token, proxy, game_id):
        response = game_claim.game_claim_points(token, proxy, game_id)
        return response

    def play_game(self, profile_id, auth_data, proxy=None):
        token = auth_requests.get_token(profile_id, auth_data, proxy)
        available_count = self.get_balance(token=token, proxy=proxy)['playPasses']
        if available_count == 0:
            print(f'{profile_id}-game | Нет кристаллов')
        else:

            for _ in range(available_count):
                game_id = self.play(profile_id, token, proxy)
                time.sleep(random.randint(30, 33))
                game_result = self.game_claim(token=token, proxy=proxy, game_id=game_id)
                balance = self.get_balance(token=token, proxy=proxy)
                current_balance = balance['availableBalance']
                playPasses = balance['playPasses']
                print(profile_id + " | " + game_id + ' ' + game_result + ' | Баланс: ' + current_balance + " | Осталось игр: "+playPasses)

    def daily(self, profile_id, auth_data, proxy=None):
        token = auth_requests.get_token(profile_id, auth_data, proxy)
        response_get = ClaimRewards.claim_rewards_get(token, proxy)
        response_post = ClaimRewards.claim_rewards_post(token, proxy)
        available_count = self.get_balance(token=token, proxy=proxy)['playPasses']
        if available_count == 0:
            print(f'{profile_id}-claim daily | Нет кристаллов')
        else:
            print(f'{profile_id}-claim daily | Имеется {available_count} повторов')

    def farming(self, profile_id, auth_data, proxy=None):
        token = auth_requests.get_token(profile_id, auth_data, proxy)
        response_claim = farming.claim_farming(token, proxy)
        print(f'{profile_id}-claim farming | {response_claim.text}')
        response_start = farming.start_farming(token, proxy)
        start_data = response_start.json()
        claim_pause = (start_data["endTime"]/1000 - int(datetime.now().timestamp()))/60
        print(f'{profile_id}-start farming| {response_start.text} | Клейм через {claim_pause} минут')


    def friend_claim(self, profile_id, auth_data, proxy=None):
        token = auth_requests.get_token(profile_id, auth_data, proxy)
        response_claim = friend_claim.claim_friend(token, proxy)
        print(f'{profile_id}-claim friend | {response_claim.text}')



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
