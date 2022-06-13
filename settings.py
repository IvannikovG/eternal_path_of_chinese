from pydantic import BaseSettings, PostgresDsn


class PgSettings(BaseSettings):
    pg_dsn: PostgresDsn = 'postgresql://root:root@127.0.0.1:5432/chinese'
