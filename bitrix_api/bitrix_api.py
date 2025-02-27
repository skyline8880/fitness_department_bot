from typing import Union

import aiohttp

from core.secrets import BitrixSecrets
from database.database import Database


class Bitrix24():
    def __init__(self, department_sign: Union[int, str]) -> None:
        self.db = Database()
        self.dep = department_sign
        self.webhook = None

    async def collect(self):
        self.webhook = BitrixSecrets(department_id=self.dep).webhook()
        return self

    async def get_bitrix_deal_list(self):
        url = f'{self.webhook}/crm.deal.list'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                return await response.json()

    async def get_deal_fields(self):
        url = f'{self.webhook}/crm.deal.fields'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                return await response.json()

    async def get_deal(self, deal_id):
        url = f'{self.webhook}/crm.deal.get'
        params = {'id': deal_id}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=params) as response:
                return await response.json()

    async def get_timeline_fields(self):
        url = f'{self.webhook}/crm.timeline.comment.fields'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                return await response.json()

    async def get_category_list(self, entity_type_id):
        params = {'entityTypeId': entity_type_id}
        url = f'{self.webhook}/crm.category.list'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=params) as response:
                return await response.json()

    async def get_conatact_list(self):
        url = f'{self.webhook}/crm.contact.list'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                return await response.json()

    async def timeline_add(self, json):
        url = f'{self.webhook}/crm.timeline.comment.add'
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=json) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['result']

    async def entity_item_add(self, json):
        url = f'{self.webhook}/entity.item.add'
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=json) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['result']

    async def create_deal(self, json):
        url = f'{self.webhook}/crm.deal.add'
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=json) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['result']

    async def update_deal(self, json):
        url = f'{self.webhook}/crm.deal.update'
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=json) as response:
                return response.status
