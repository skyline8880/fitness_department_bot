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
import pandas as pd

setlocale(LC_ALL, 'ru_RU.utf-8')


async def main():
    db = Database()
    start_date = dt.datetime(year=2024, month=1, day=10, hour=10, minute=0, second=0)
    end_date = dt.datetime(year=2024, month=1, day=20, hour=10, minute=0, second=0)
    date_range = pd.date_range(start=start_date, end=end_date).tolist()
    #events_to_send = await db.select_new_user_events_to_send(telegram_id=1058269375)
    for i in range(10):
        for j in range(1, 6):
            for dtime in date_range:

                ev = {
                    'message_id': None,
                    'creator': 1058269375,
                    'department_id': 2,
                    'subdivision_id': j,
                    'event_date': dtime,
                    'name': f'test{i}',
                    'description': f'test{i} (desc)',
                    'is_free': True,
                }
                await db.insert_event(data=ev)
    #recieve_list = await db.select_event_recievers_list(event_id=8)
    #comming_events_list = await db.select_comming_events_by_sent_status(was_sent=True)
    #lspd = await db.select_new_user_events_to_send(telegram_id=1058269375)
    #chk = await db.check_users_dep_and_subdiv(department_id=1, subdivision_id=2, telegram_id=1058269375)
    #print(recieve_list)
    #print(comming_events_list)
    #print(lspd)
    #if chk is not None:
    #    print(chk)
    


if __name__ == '__main__':
    asyncio.run(main=main())