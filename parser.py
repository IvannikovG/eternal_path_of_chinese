from telethon.sync import TelegramClient, events
from pprint import pprint
import json
from resources import Message

api_id = 19763055
api_hash = 'e9fb0c49341d086e93f64db02abdf3c3'
chat_id = -1001680578245


def get_by_index(arr, index):
    try:
        el = arr[index]
        return el
    except IndexError:
        return ""


def check_has_id(string: str) -> bool:
    if not string:
        return False
    else:
        idx = string.split(" ")[0]
        return idx.isdigit()


with TelegramClient('name', api_id, api_hash) as client:
    messages = client.get_messages(chat_id, limit=1000)
    x = [mes.message for mes in messages]
    print("Logging: ", "Unfiltered messages", len(x))


def parse_langs(lang_array: list) -> dict:
    lang_dict = {'ru': [], 'en': [], 'de': [], 'srb': [], 'esp': []}
    for i in lang_array:
        try:
            lang, word = i.split(':')
            lang_dict[lang] = lang_dict[lang.strip()] + [word.strip()]
        except ValueError:
            ru_word = i.split(':')[0]
            lang_dict['ru'] = lang_dict['ru'] + [ru_word.strip()]
    return lang_dict


def parse_translation(translation: str) -> dict:
    split_header = translation.split("/")
    translation = parse_langs(split_header)
    return translation


def parse_header(header: str) -> dict:
    split_header = header.split("-")
    hieroglyph_id = split_header[0].strip()
    chinese = split_header[1].strip()
    pinyin = split_header[2].strip()
    translation = get_by_index(split_header, 3)
    parsed_translation = parse_translation(translation)
    return {'hieroglyph_id': hieroglyph_id,
            'chinese': chinese,
            'pinyin': pinyin,
            'translation': parsed_translation}


def valid_line(line: str) -> bool:
    if not line:
        return False
    else:
        return True


def parse_line(line):
    print("LINE", line)
    if not valid_line(line):
        return None
    elif line.startswith('#rule'):
        return {'rule': line}
    split_line = line.split("-")
    chinese = split_line[0].strip()
    pinyin = split_line[1].strip()
    translation = get_by_index(split_line, 2)
    parsed_translation = parse_translation(translation)
    return {'chinese': chinese,
            'pinyin': pinyin,
            'translation': parsed_translation}


def parse_lines(lines):
    parsed_lines = []
    for line in lines:
        parsed_lines.append(parse_line(line))
    return parsed_lines


def parse_message(message: str) -> dict:
    message_lines = message.split("\n")
    header, *lines = message_lines
    examples = list(filter(lambda el: el, parse_lines(lines)))
    return {'resource': parse_header(header),
            'examples': examples}


filtered_messages = [message for message in x if check_has_id(message)]
print("Logging: ", "Filtered messages", len(filtered_messages))

result_json = []
for message in filtered_messages:
    result_json.append(parse_message(message))


res = json.dumps(result_json)


with open('resources.json', 'w', encoding='utf-8') as file:
    js = file.write(res)

with open('resources.json', 'r', encoding='utf-8') as file:
    j = file.read()

for item in json.loads(j):
    m = Message(**item)
    print(m.resource.translation)