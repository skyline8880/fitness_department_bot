from typing import Any, Dict, Union

import aiohttp

from core.secrets import BitrixSecrets
from database.database import Database


class Bitrix24():
    def __init__(self, department_sign: Union[int, str]) -> None:
        self.db = Database()
        self.dep = department_sign
        self.webhook = None

    async def params_form(
            self,
            keys: list,
            params: Dict[str, Any]) -> str:
        result = ''
        for key in keys:
            if isinstance(params[key], list):
                for n, lv in enumerate(params[key]):
                    result += f'{key}[{n}]={lv}&'
            elif isinstance(params[key], dict):
                for k, dv in params[key].items():
                    if isinstance(dv, list):
                        for n, lv in enumerate(dv):
                            result += f'{key}[{k}][{n}]={lv}&'
                    else:
                        result += f'{key}[{k}]={dv}&'
            else:
                result += f'{key}={params[key]}&'
        return result

    async def collect(self):
        self.webhook = BitrixSecrets(department_id=self.dep).webhook()
        return self

    async def get_bitrix_deal_list(self, **params):
        url = f'{self.webhook}/crm.deal.list'
        str_params = await self.params_form(keys=params.keys(), params=params)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=str_params) as response:
                return await response.json()

    async def get_deal_fields(self, **params):
        url = f'{self.webhook}/crm.deal.fields'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                return await response.json()

    async def get_deal(self, **params):
        url = f'{self.webhook}/crm.deal.get'
        str_params = await self.params_form(keys=params.keys(), params=params)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=str_params) as response:
                return await response.json()

    async def get_timeline_fields(self, **params):
        url = f'{self.webhook}/crm.timeline.comment.fields'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                return await response.json()

    async def get_category_fields(self, **params):
        url = f'{self.webhook}/crm.category.fields'
        str_params = await self.params_form(keys=params.keys(), params=params)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=str_params) as response:
                return await response.json()

    async def get_category_stage_list(self, **params):
        url = f'{self.webhook}/crm.dealcategory.stage.list'
        str_params = await self.params_form(keys=params.keys(), params=params)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=str_params) as response:
                return await response.json()

    async def get_category_list(self, **params):
        url = f'{self.webhook}/crm.category.list'
        str_params = await self.params_form(keys=params.keys(), params=params)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=str_params) as response:
                return await response.json()

    async def get_conatact_list(self, **params):
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
