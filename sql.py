import psycopg2
from psycopg2.extras import DictCursor
from settings import PgSettings
from sqlalchemy import insert
import json
from psycopg2.extensions import register_adapter
from psycopg2.extras import Json
from model import chinese_record


def query_db(query):
    with psycopg2.connect(dsn=PgSettings().pg_dsn, cursor_factory=DictCursor) as pg_conn:
        curs = pg_conn.cursor()
        curs.execute(query)
        rows = curs.fetchall()
        return rows


def load_json_to_db(j_obj):
    with psycopg2.connect(dsn=PgSettings().pg_dsn, cursor_factory=DictCursor) as pg_conn:
        curs = pg_conn.cursor()
        for item in j_obj:
            my_json = json.dumps(item)
            insert_query = "insert into chinese_record (resource) values (%s) returning resource"
            curs.execute(insert_query, (my_json,))
            print(curs.fetchone()[0])

    print("OK, INSERTED!")
    return "OK, inserted"


with open('resources.json', 'r', encoding='utf-8') as file:
    j = file.read()

load_json_to_db(json.loads(j))
