import time
import os
import json
from datetime import datetime
from telethon.sync import TelegramClient
from parser import *


api_id = 19763055
api_hash = 'e9fb0c49341d086e93f64db02abdf3c3'
chat_id = -1001680578245


# with open('resources.json', 'r', encoding='utf-8') as file:
#     j = file.read()

def test_job_1():
    print(" TEST JOB 1 RUNNING")
    time.sleep(5)
    print(" TEST JOB 1 OK")


def test_job_2():
    print(" TEST JOB 2 RUNNING")
    time.sleep(3)
    print(" TEST JOB 2 OK")


def test_job_3():
    print(" TEST JOB 3 RUNNING")
    time.sleep(2)
    print(" TEST JOB 3 OK")


def sync_messages_json():
    with TelegramClient('name', api_id, api_hash) as client:
        messages = client.get_messages(chat_id, limit=10)
        x = [(mes.message, mes.date.isoformat()) for mes in messages]
        print(x)
        print("Logging: ", "Unfiltered messages", len(x))
        filtered_messages = [(m, date) for m, date in x if check_has_id(m)]
        print("Logging: ", "Filtered messages", len(filtered_messages))
        try:
            with open('resources.json', 'w', encoding='utf-8') as file:
                result_json = []
                for message in filtered_messages:
                    result_json.append(parse_message(message))
                    print("="*30)
                    print(parse_message(message))
                    print("="*30)
                res = json.dumps(result_json, indent=4, sort_keys=True, ensure_ascii=False)
                js = file.write(res)
                print("Logging: ", file.name, " saved.")
        except Exception:
            print("Logging: Can not produce js file")


global_jobs = [{"name": "test_job_1",
                "action": test_job_1.__name__,
                "type": "periodic",
                "locked": 'false',
                "status": 'active',
                'period': 1},
               {"name": "test_job_2",
                "action": test_job_2.__name__,
                "type": "periodic",
                "locked": 'false',
                "status": 'active',
                'period': 2},
               {"name": "test_job_3",
                "action": test_job_3.__name__,
                "type": "periodic",
                "locked": 'false',
                "status": 'active',
                'period': 3}]



