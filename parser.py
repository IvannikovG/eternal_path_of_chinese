from typing import Dict, Union


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
    l_a = [s.strip() for s in lang_array]
    for i in l_a:
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


def parse_line(line:str) -> Dict[str, Union[dict, str]]:
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


def parse_graphemes(line:str) -> list:
    _, graphemes = line.split(":")
    graphemes_list = graphemes.split("-")
    return graphemes_list


def contains_graphemes_bool(lines: list) -> bool:
    try:
        return lines[-1].startswith("graphemes")
    except:
        return False


def parse_lines(lines: list) -> tuple:
    parsed_lines = []
    contains_graphemes = contains_graphemes_bool(lines)
    if contains_graphemes:
        graphemes = parse_graphemes(lines[-1])
        for line in lines[:-1 or None]:
            parsed_lines.append(parse_line(line))
        return graphemes, parsed_lines
    else:
        for line in lines:
            parsed_lines.append(parse_line(line))
        return "No graphemes", parsed_lines


def parse_message(message_info: tuple) -> dict:
    message, created = message_info
    message_lines = message.split("\n")
    header, *lines = message_lines
    graphemes, parsed_lines = parse_lines(lines)
    examples = list(filter(lambda el: el, parsed_lines))
    message_template = {'resource': parse_header(header),
                        'examples': examples,
                        'created': created}
    if graphemes == "No graphemes":
        return message_template
    else:
        message_template['graphemes'] = graphemes
        return message_template
