import asyncio
import calendar
import datetime as dt
from locale import LC_ALL, setlocale
from typing import Any, Dict, List, Tuple, Union

from dateutil.relativedelta import relativedelta
from psycopg.errors import UniqueViolation

from database.connection.create_connect import DatabaseConnection
from database.database import Database
from database.queries.create import CREATE, DEFAULT_INSERT, DROP_SCHEMA

setlocale(LC_ALL, 'ru_RU.utf-8')


async def main():
    now = dt.datetime.now()
    print(dt.datetime.strftime(now, '%d.%m.%Y'))
    cl = calendar.monthcalendar(year=now.year, month=now.month)
    weeks = calendar.weekheader(width=2)
    print(now + relativedelta(years=1))

"""     db = Database()
    con = await db.connection()
    cur = con.cursor()
    await cur.execute('''SELECT department_id, subdiv_references FROM fit.user;''')
    l1 = await cur.fetchall()
    print(l1[0])
    con = await db.connection()
    cur = con.cursor()
    await cur.execute('''insert into fit.user (phone, telegram_id) values ('79998533965', 1058269375)''')
    await con.commit() """
    


if __name__ == '__main__':
    asyncio.run(main=main())