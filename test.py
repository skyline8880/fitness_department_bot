import asyncio
import calendar
import datetime as dt
from locale import LC_ALL, setlocale
from typing import Any, Dict, List, Tuple, Union

import pandas as pd
from dateutil.relativedelta import relativedelta
from psycopg.errors import UniqueViolation

from database.connection.create_connect import DatabaseConnection
from database.database import Database
from database.queries.create import CREATE, DEFAULT_INSERT, DROP_SCHEMA

setlocale(LC_ALL, 'ru_RU.utf-8')


async def main():
    db = Database()
    start_date = dt.datetime(year=2025, month=1, day=10, hour=10, minute=0, second=0)
    end_date = dt.datetime(year=2025, month=1, day=20, hour=10, minute=0, second=0)
    ks = dt.datetime.strftime(start_date, '%d %B %Y').lower()
    print(ks)

if __name__ == '__main__':
    asyncio.run(main=main())