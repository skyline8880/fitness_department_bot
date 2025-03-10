import asyncio
import locale
import os
import sys

from dotenv import load_dotenv

load_dotenv()

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


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


class BitrixSecrets():
    def __init__(self, department_id):
        self.departments = {
            1: os.getenv('MSK'),
            2: os.getenv('VLK'),
            3: os.getenv('NKR'),
            4: os.getenv('BTV')
        }
        self.webhook_ = self.departments[department_id]

    def webhook(self):
        return self.webhook_
