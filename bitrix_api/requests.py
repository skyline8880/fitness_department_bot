import datetime as dt
from typing import Union

from bitrix_api.bitrix_api import Bitrix24
from bitrix_api.bitrix_params import (create_contact, create_deal,
                                      timeline_add_on_action,
                                      update_deal_stage)
from core.secrets import TelegramSectrets
from database.database import Database


async def send_bitrix_request(
        telegram_id: Union[int, str],
        event_id: Union[int, str],
        act_id: Union[int, str],
        act_name: str):
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
    if patronymic is None:
        patronymic = ''
    date = dt.datetime.strftime(event_date, '%d.%m.%Y')
    time = dt.datetime.strftime(event_date, '%H:%M')
    deal_id = await db.select_current_customer_deal_id(
        event_id=event_id,
        customer_id=telegram_id)
    bx24 = await Bitrix24(department_sign=department_id).collect()
    comment = (
            f'пользователь выбрал активность: {act_name}')
    if deal_id is None:
        if int(act_id) == 2:
            return
        get_contact = await bx24.get_duplicates(
            entity_type='CONTACT',
            type='PHONE',
            values=[phone])
        if 'error' in get_contact.keys():
            print('GET CONTACT ERROR', get_contact)
            return
        contact_ids = None
        if get_contact['result'] == []:
            created_contact = await bx24.create_contact(
                json=create_contact(
                    last_name=last_name,
                    first_name=first_name,
                    patronymic=patronymic,
                    phone=phone))
            if 'error' in created_contact.keys():
                print('CREATE CONTACT ERROR', created_contact)
                return
            contact_ids = [created_contact['result']]
        else:
            contact_ids = get_contact['result']['CONTACT']
        deal_id = await bx24.create_deal(
            json=create_deal(
                title=(
                    f'{event_name} ({date} в {time}) - '
                    f'{last_name} {first_name} {patronymic}'),
                assigned_by=bx24.deal_direct['assigned'],
                category_id=bx24.deal_direct['category_id'],
                stage_id=bx24.deal_direct['new'],
                contact_ids=contact_ids))
        await db.update_enroll_deal_id(
            event_id=event_id,
            customer_id=telegram_id,
            deal_id=deal_id)
        comment = (
            'Cделка создана ботом: Ohana Сеть Фитнес события'
            f' - {TelegramSectrets.BOT_USERNAME}\n'
            f'пользователь: {last_name} {first_name} {patronymic}\n'
            f'с номером телефона: {phone}\n'
            f'выбрал активность: {act_name}\n'
            f'по мероприятию: {event_name}\n'
            f'которое будет проходить: {date} в {time}\n'
            f'в пдразделении: {subdivision}')
    else:
        if int(act_id) == 2:
            await bx24.update_deal(
                json=update_deal_stage(
                    deal_id=deal_id,
                    stage_id=bx24.deal_direct['cancel']))
        else:
            await bx24.update_deal(
                json=update_deal_stage(
                    deal_id=deal_id,
                    stage_id=bx24.deal_direct['new']))
    await bx24.timeline_add(
        json=timeline_add_on_action(
            deal_id=deal_id,
            comment=comment))
