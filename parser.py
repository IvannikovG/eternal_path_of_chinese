from typing import Dict, Union
from unidecode import unidecode

pluck = lambda d, *args: (d[arg] for arg in args)


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
    if len(lang_array) != 1:
        try:
            lang_dict = {'ru': [], 'en': [], 'de': [], 'srb': [], 'esp': []}
            l_a = [s.strip() for s in lang_array]
            if len(l_a) == 1:
                lang_dict['ru'] = lang_dict['ru'] + l_a[0].strip()
            else:
                for i in l_a:
                    if ":" in i:
                        lang, word = i.split(':')
                        lang_dict[lang] = lang_dict[lang.strip()] + [word.strip()]
                    else:
                        ru_word = i
                        lang_dict['ru'] = lang_dict['ru'] + [ru_word.strip()]
            return lang_dict
        except Exception as e:
            print("Exception in parse langs: ", e)
    else:
        return {'ru': lang_array[0]}


def parse_translation(translation: str) -> dict:
    try:
        split_line = translation.split("/")
        translation = parse_langs(split_line)
        return translation
    except Exception as e:
        print("Exception in parse translation: ", e)


def parse_header(header: str) -> dict:
    split_header = header.split("-")
    hieroglyph_id = split_header[0].strip()
    chinese = split_header[1].strip()
    pinyin = split_header[2].strip()
    translation = get_by_index(split_header, 3)
    parsed_translation = parse_translation(translation)
    return {'hieroglyph_id': hieroglyph_id,
            'chinese': chinese,
            'raw_pinyin': unidecode(chinese).lower().strip(),
            'pinyin': pinyin,
            'translation': parsed_translation}


def valid_line(line: str) -> bool:
    if not line:
        return False
    elif not line.strip():
        return False
    else:
        return True


def parse_line(line: str) -> Dict[str, Union[dict, str]]:
    try:
        if not valid_line(line):
            return None
        elif line.startswith('#rule'):
            return {'rule': line}
        stripped_line = line.strip()
        split_line = stripped_line.split("-")
        chinese = split_line[0].strip()
        pinyin = split_line[1].strip()
        translation = get_by_index(split_line, 2)
        parsed_translation = parse_translation(translation)
        return {'chinese': chinese,
                'pinyin': pinyin,
                'translation': parsed_translation}
    except Exception as e:
        print("Exception in parse parse line: ", e)


def parse_graphemes(line: str) -> list:
    try:
        _, graphemes = line.split(":")
        graphemes_list = list(map(lambda el: el.strip(), graphemes.split("-")))
        return graphemes_list
    except Exception as e:
        print("Exception in parse parse graphemes: ", e)


def contains_graphemes_bool(lines: list) -> bool:
    try:
        return lines[-1].startswith("graphemes")
    except:
        return False


def parse_lines(lines: list) -> tuple:
    try:
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
    except Exception as e:
        print("Exception in parse lines: ", e)


def parse_g_header(header: str) -> dict:
    split_header = header.split("-")
    hieroglyph_id = split_header[0].strip()
    chinese = split_header[1].strip()
    pinyin = split_header[2].strip()
    translation = get_by_index(split_header, 3)
    parsed_translation = parse_translation(translation)
    return {'hieroglyph_id': hieroglyph_id,
            'chinese': chinese,
            'raw_pinyin': unidecode(chinese).lower().strip(),
            'pinyin': pinyin,
            'translation': parsed_translation}


def parse_alternative(line: str) -> list:
    _, alt = line.split(":")
    alternative = [line.strip() for line in alt.split('-')]
    return alternative


def contains_alternative_bool(lines: list) -> bool:
    try:
        return lines[0].startswith("alternative")
    except Exception as e:
        return False


def parse_g_lines(lines: list) -> dict:
    try:
        contains_alternative = contains_alternative_bool(lines)
        if contains_alternative:
            alternative = parse_alternative(lines[0])
            return {'additional': alternative,
                    'type': lines[1].split(":")[1].strip()}

        else:
            return {'type': lines[0].split(":")[1].strip()}
    except Exception as e:
        print("Exception in parse GG lines: ", e)


def build_g_res(header: dict, lines: dict) -> dict:
    chinese = header.get('chinese')
    new_chinese = {}
    t = lines.get('type')
    alt = lines.get('additional')
    new_chinese['general'] = chinese
    if alt is not None:
        new_chinese['additional'] = alt
    header['chinese'] = new_chinese
    header['type'] = t
    return header


def parse_g(message_info: tuple) -> dict:
    message, created = message_info
    message_lines = [line for line in message.split('\n') if line.strip() != '']
    header, *lines = message_lines
    g_header = parse_g_header(header)
    g_lines = parse_g_lines(lines)
    return {'resource': (build_g_res(g_header, g_lines))}


def parse_message(message_info: tuple) -> dict:
    print("==============================")
    try:
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
    except Exception as e:
        print("Exception in parse message: ", e)
