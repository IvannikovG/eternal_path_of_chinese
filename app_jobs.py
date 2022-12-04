import time
import os
import json
from telethon.sync import TelegramClient
from parser import *
from types import SimpleNamespace
from typing import BinaryIO
import pypandoc


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
    api_id = 19763055
    api_hash = 'e9fb0c49341d086e93f64db02abdf3c3'
    chat_id = -1001680578245
    with TelegramClient('name', api_id, api_hash) as client:
        messages = client.get_messages(chat_id, limit=5000)
        x = [(mes.message, mes.date.isoformat()) for mes in messages]
        print("Logging: ", "Unfiltered messages", len(x))
        filtered_messages = [(m, date) for m, date in x if check_has_id(m)]
        print("Logging: ", "Filtered messages", len(filtered_messages))
        try:
            with open('resources.json', 'w', encoding='utf-8') as file:
                result_json = []
                for message in filtered_messages:
                    parsed_message = parse_message(message)
                    print(parsed_message)
                    result_json.append(parsed_message)
                res = json.dumps(result_json, indent=4, sort_keys=True, ensure_ascii=False)
                js = file.write(res)
                print("Logging: ", file.name, " saved." " Total count: ", len(filtered_messages))
        except Exception as e:
            print("Logging: Can not produce js file: ", e)


def create_md_file(line: Dict) -> BinaryIO:
    md_content = pypandoc.convert_text(json.dumps(line), 'json', 'md', outputfile="base/somefile.md")
    print(md_content)
    return md_content


def save_md_file(md_file: BinaryIO):
    print("SAVING")
    return


def sync_messages_to_mds_from_json():
    try:
        with open('resources.json', 'r', encoding='utf-8') as file:
            f = json.load(file)
            print(f)
            for line in f:
                md_file = create_md_file(line)
                save_md_file(md_file)
                print("++++++++++++++")
            return 1
    except Exception:
        print("FALSE")
        return 2


if __name__ == '__main__':
    sync_messages_json()
    print ("Synced messages!")
    print(unidecode("谢谢你"))


# global_jobs = [{"name": "test_job_1",
#                 "action": test_job_1.__name__,
#                 "type": "periodic",
#                 "locked": 'false',
#                 "status": 'active',
#                 'period': 1},
#                {"name": "test_job_2",
#                 "action": test_job_2.__name__,
#                 "type": "periodic",
#                 "locked": 'false',
#                 "status": 'active',
#                 'period': 2},
#                {"name": "test_job_3",
#                 "action": test_job_3.__name__,
#                 "type": "periodic",
#                 "locked": 'false',
#                 "status": 'active',
#                 'period': 3}]