import psycopg2
from psycopg2.extras import DictCursor
from settings import PgSettings
from sqlalchemy import insert
import json
from uuid import uuid1
from resources import Message, Job

model_matcher = {"Job": Job,
                 "Message": Message}


def query_db(query):
    with psycopg2.connect(dsn=PgSettings().pg_dsn, cursor_factory=DictCursor) as pg_conn:
        curs = pg_conn.cursor()
        curs.execute(query)
        rows = curs.fetchall()
        result = []
        for row in rows:
            result.append(dict(**row))
        return result


def exec_db(query):
    with psycopg2.connect(dsn=PgSettings().pg_dsn, cursor_factory=DictCursor) as pg_conn:
        curs = pg_conn.cursor()
        curs.execute(query)
        pg_conn.commit()
    return True


def update_resource(resourceType, idx, resource):
    with psycopg2.connect(dsn=PgSettings().pg_dsn, cursor_factory=DictCursor) as pg_conn:
        curs = pg_conn.cursor()
        update_res = "update {resourceType} ".format(resourceType=resourceType)
        set_part = "set resource = %s where id = %s returning resource;"
        query = update_res + set_part
        res = json.dumps(resource, default=str)
        # print('QQ', query)
        curs.execute(query, (res, idx,))
        pg_conn.commit()
        return curs.fetchall()


def insert_resource(resourceType: str, resource: dict) -> dict:
    with psycopg2.connect(dsn=PgSettings().pg_dsn, cursor_factory=DictCursor) as pg_conn:
        curs = pg_conn.cursor()
        model = model_matcher[resourceType]
        try:
            model(**resource)
            res = json.dumps(resource)
            insert_part = "insert into %s (id, resource)" % resourceType
            values_part = "values (%s, %s) returning resource"
            insert_query = insert_part + values_part
            idx = str(uuid1())
            curs.execute(insert_query, (idx, res,))
            print("OK, INSERTED!")
            return resource
        except Exception:
            print(model(**resource))
            print("Logging: ", resource, "failed validation")
            return resource


def load_json_to_db(j_obj):
    with psycopg2.connect(dsn=PgSettings().pg_dsn, cursor_factory=DictCursor) as pg_conn:
        curs = pg_conn.cursor()
        truncate_query = "truncate chinese_record"
        curs.execute(truncate_query)
        for item in j_obj:
            my_json = json.dumps(item)
            insert_query = "insert into chinese_record (resource, ts) values (%s, now()) returning resource"
            curs.execute(insert_query, (my_json,))
            print(curs.fetchone()[0])

    print("OK, INSERTED!")
    return "OK, inserted"


def create_table(resourceType: str) -> None:
    exec_db(
        """create table if not exists %s
           (id            text            primary key not null,
            cts           timestamp       with time zone default current_timestamp,
            ts            timestamp       with time zone default current_timestamp,
            resource_type text            default '%s'::text,
            resource      jsonb           not null)""" % (resourceType, resourceType))


with open('resources.json', 'r', encoding='utf-8') as file:
    j = file.read()
    load_json_to_db(json.loads(j))
