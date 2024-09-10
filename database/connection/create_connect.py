import psycopg

from core.secrets import DBSecrets


class DatabaseConnection():
    async def __call__(self) -> psycopg.AsyncConnection:
        self.connect = await psycopg.AsyncConnection.connect(
            host=DBSecrets.PGHOST,
            dbname=DBSecrets.PGDATABASE,
            user=DBSecrets.PGUSERNAME,
            password=DBSecrets.PGPASSWORD,
            port=DBSecrets.PGPORT
        )
        return self.connect
