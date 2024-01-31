import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
from unidecode import unidecode
import pinyin
import chinese_converter


def parse_one_hanzi_page(page_uri):
    URL = page_uri
    headers = {'Accept-Encoding': 'identity'}
    r = requests.get(url=URL, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    table_content = soup.find_all('tr')

    acc = []
    acc2 = []
    acc3 = []

    for row in table_content:
        if not row.find_all('th'):
            acc.append(row.find_all('td'))
        else:
            acc.append(row.find_all('th'))

    for a in acc:
        mini_acc = []
        for cell in a:
            try:
                parsed_1 = BeautifulSoup(re.search(r'<th>(.*?)</th>', str(cell)).group(1), features='html.parser')
                if '</span>' in str(parsed_1):
                    parsed = parsed_1.span.get_text()
                    mini_acc.append(parsed.replace('General Standard#', 'Id in Standard specification'))
                else:
                    mini_acc.append(parsed_1)
            except Exception:
                parsed_1 = BeautifulSoup(re.search(r'<td>(.*?)</td>', str(cell)).group(1), features='html.parser')
                if 'span' in str(parsed_1):
                    parsed = parsed_1.span.get_text()
                    mini_acc.append(parsed)
                elif '</a>' in str(parsed_1):
                    parsed = parsed_1.a.get_text()
                    mini_acc.append(parsed)
                else:
                    mini_acc.append(parsed_1)
        acc2.append(mini_acc)

    for row in acc2:
        mini_acc = []
        for cell in row:
            if str(cell) == '':
                mini_acc.append('N/A')
            else:
                text = str(cell)
                decoded_text = text.encode('iso-8859-1').decode('utf-8')
                decoded_text = decoded_text.replace(", ", "/")
                decoded_text = decoded_text.replace("; ", "/")
                mini_acc.append(decoded_text)
        acc3.append(mini_acc)

    return acc3


def sync_hanzidb():
    URL = 'http://hanzidb.org/character-list/hsk?page='
    base_url = URL
    csv_file = 'hanzidb_output.csv'
    first_page = parse_one_hanzi_page(base_url)
    headers = first_page[0]
    # first write to csv
    with open(csv_file, 'w', newline='') as file:
        rows = first_page[1:]
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)
    # now iterate and append without headers
        for i in range(2, 28):
            url = base_url + str(i)
            page = parse_one_hanzi_page(url)
            print(url, page[1])
            rows = page[1:]
            writer = csv.writer(file)
             # Write data
            writer.writerows(rows)
    df = pd.read_csv('hanzidb_output.csv')
    df['converted_pinyin'] = df.apply(lambda x: pinyin.get(x[0].lower().strip(), format="numerical", delimiter=" "), axis=1)
    df['raw_pinyin'] = df.apply(lambda x: unidecode(str(x['N/A'])).lower().strip(), axis=1)
    df['simplified_chinese'] = df.apply(lambda x: chinese_converter.to_simplified(str(x['Radical'])), axis=1)
    df = df.rename(columns={'Stroke count': 'stroke_count', 'HSK level': 'hsk_level',
                            'Frequency rank': 'frequency_rank',
                            'Id in Standard specification': 'id_in_standard_specification'})
    df.to_csv('hanzidb_output.csv', index=False)


if __name__ == '__main__':
    print("Syncing HanziDB!")
    # sync_hanzidb()
    df = pd.read_csv('hanzidb_output.csv')
    # df['raw_pinyin'] = df.apply(lambda x: unidecode(str(x['N/A'])).lower().strip(), axis=1) #unidecode(str(x['N/A'])).lower().strip())
    print(df['simplified_chinese'].unique())
    print('Haha: OK', "谢谢你")
