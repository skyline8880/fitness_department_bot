from typing import Any, Dict, Union

import aiohttp

from bitrix_api.bitrix_categories import DealDirection
from core.secrets import BitrixSecrets
from database.database import Database


class Bitrix24():
    def __init__(self, department_sign: Union[int, str]) -> None:
        self.db = Database()
        self.dep_sign = department_sign
        self.dep_id = None
        self.dep_name = None
        self.webhook = None
        self.deal_direct = None

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
        """ db = Database()
        self.dep_id, self.dep_name = await db.select_department_by_sign(
            sign=self.dep_sign) """
        self.dep_id = self.dep_sign
        self.webhook = BitrixSecrets(department_id=self.dep_id).webhook()
        self.deal_direct = DealDirection(
            department_id=self.dep_id).get_direction()
        return self

    async def get_item_list(self, **params):
        url = f'{self.webhook}/crm.item.list'
        str_params = await self.params_form(keys=params.keys(), params=params)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=str_params) as response:
                return await response.json()

    async def get_type_list(self, **params):
        url = f'{self.webhook}/crm.type.list'
        str_params = await self.params_form(keys=params.keys(), params=params)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=str_params) as response:
                return await response.json()

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

    async def get_category_by_id(self, **params):
        url = f'{self.webhook}/crm.category.get'
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

    async def get_dealcategory_list(self, **params):
        url = (f"{self.webhook}/crm.dealcategory.list")
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

    async def get_contact(self, **params):
        url = f'{self.webhook}/crm.contact.get'
        str_params = await self.params_form(keys=params.keys(), params=params)
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, params=str_params) as response:
                return await response.json()

    async def get_duplicates(self, **params):
        url = f'{self.webhook}/crm.duplicate.findbycomm'
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=params) as response:
                return await response.json()

    async def get_contact_list(self, **params):
        url = f'{self.webhook}/crm.contact.list'
        str_params = await self.params_form(keys=params.keys(), params=params)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=str_params) as response:
                return await response.json()

    async def entity_merge(self, json):
        url = f'{self.webhook}/crm.entity.mergeBatch'
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=json) as response:
                return await response.json()

    async def create_contact(self, json):
        url = f'{self.webhook}/crm.contact.add'
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=json) as response:
                return await response.json()

    async def delete_contact(self, **params):
        url = f'{self.webhook}/crm.contact.delete'
        str_params = await self.params_form(keys=params.keys(), params=params)
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, params=str_params) as response:
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

    async def get_user(self, **params):
        url = f'{self.webhook}/user.get'
        print(url)
        str_params = await self.params_form(keys=params.keys(), params=params)
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=str_params) as response:
                return await response.json()

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
