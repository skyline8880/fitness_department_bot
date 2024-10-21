import asyncio
import locale
import os
import sys

from dotenv import load_dotenv

load_dotenv()

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class DBSecrets:
    PGHOST = os.getenv('PGHOST')
    PGDATABASE = os.getenv('PGDATABASE')
    PGUSERNAME = os.getenv('PGUSERNAME')
    PGPASSWORD = os.getenv('PGPASSWORD')
    PGPORT = os.getenv('PGPORT')
    SCHEMA_NAME = os.getenv('SCHEMA_NAME')


class TelegramSectrets:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    BOT_USERNAME = os.getenv('BOT_USERNAME')
    DEVELOPER = int(os.getenv('DEVELOPER'))
