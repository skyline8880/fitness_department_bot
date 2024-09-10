from psycopg.errors import UniqueViolation

from database.connection.create_connect import DatabaseConnection
from database.queries.create import CREATE, DEFAULT_INSERT, DROP_SCHEMA


class StructureBuilder():
    def __init__(self) -> None:
        self.connection = DatabaseConnection()

    async def create(self) -> None:
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(CREATE)
        print('created')
        await con.commit()
        await con.close()

    async def default_insert(self):
        con = await self.connection()
        cur = con.cursor()
        try:
            await cur.execute(DEFAULT_INSERT)
            print('default data added successful')
        except UniqueViolation:
            await con.rollback()
            print('default data was added once')
        except Exception as e:
            await con.rollback()
            print(f'another error: {e}')
        finally:
            await con.commit()
            await con.close()

    async def drop_schema(self):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(DROP_SCHEMA)
        print('schema was droped')
        await con.commit()
        await con.close()
