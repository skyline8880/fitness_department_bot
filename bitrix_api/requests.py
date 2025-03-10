from typing import Union

from bitrix_api.bitrix_api import Bitrix24
from bitrix_api.bitrix_params import create_contact
from database.database import Database


async def send_bitrix_request(
        telegram_id: Union[int, str],
        event_id: Union[int, str],
        act_id: Union[int, str]):
    db = Database()
    (
        event_id,
        event_date,
        creator_telegram_id,
        creator_lname,
        creator_fname,
        creator_phone,
        department_id,
        department,
        subdivision_id,
        subdivision,
        event_name,
        event_description,
        event_isfree,
        event_isactive,
        event_sent,
        _
    ) = await db.select_event_by_id(event_id=event_id)
    (
        user_id,
        is_admin,
        phone,
        last_name,
        first_name,
        patronymic,
        user_telegram_id,
        fullname,
        username,
        _,
        _
    ) = await db.select_user_by_sign(sign=telegram_id)
    deal_id = await db.select_current_customer_deal_id(
        event_id=event_id,
        customer_id=telegram_id
    )
    bx24 = await Bitrix24(department_sign=department_id).collect()
    if isinstance(deal_id, tuple):
        if deal_id[0] is None:
            if int(act_id) == 2:
                return
            get_contact = await bx24.get_duplicates(
                entity_type='CONTACT',
                type='PHONE',
                values=[phone],
            )
            if 'error' in get_contact.keys():
                print('GET CONTACT ERROR', get_contact)
                return
            print(get_contact)
            contact_ids = None
            if get_contact['result'] == []:
                created_contact = await bx24.create_contact(
                    json=create_contact(
                        last_name=last_name,
                        first_name=first_name,
                        patronymic=patronymic,
                        phone=phone
                    ))
                if 'error' in created_contact.keys():
                    print('CREATE CONTACT ERROR', created_contact)
                    return
                contact_ids = [created_contact['result']]
            else:
                contact_ids = get_contact['result']['CONTACT']
            print(contact_ids)
