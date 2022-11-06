from db import Base
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Boolean, Column, Integer, String


class ChineseRecord(Base):
    __tablename__ = "chinese_record"

    id = Column('id', Integer, primary_key=True, index=True)
    ts = Column('ts', TIMESTAMP, index=True, server_default=text('NOW()'))
    resource = Column('resource', JSONB)