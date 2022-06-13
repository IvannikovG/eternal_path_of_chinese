from sqlalchemy import create_engine, MetaData, Table, Column, Integer, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import JSONB
from settings import PgSettings

engine = create_engine(PgSettings().pg_dsn, echo=True)
meta = MetaData()

chinese_record = Table(
    'chinese_record', meta,
    Column('id', Integer, primary_key=True),
    Column('ts', TIMESTAMP, server_default=text('NOW()')),
    Column('resource', JSONB)
)

meta.create_all(engine)
