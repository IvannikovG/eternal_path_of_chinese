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


def parse_line(line:str) -> dict:
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


def parse_lines(lines: list) -> list:
    parsed_lines = []
    for line in lines:
        parsed_lines.append(parse_line(line))
    return parsed_lines


def parse_message(message_info: tuple) -> dict:
    message, created = message_info
    message_lines = message.split("\n")
    header, *lines = message_lines
    examples = list(filter(lambda el: el, parse_lines(lines)))
    return {'resource': parse_header(header),
            'examples': examples,
            'created': created}
