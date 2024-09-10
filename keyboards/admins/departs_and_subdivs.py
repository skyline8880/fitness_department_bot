from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.database import Database
from filters.callback_filters import (AdminMenuActions, AdminMenuActionsCD,
                                      EventDepartment, EventSubdivision)


async def department_keydoard():
    db = Database()
    departments_buttons = []
    for dep_id, dep_name in await db.select_departments():
        departments_buttons.append(
            [
                InlineKeyboardButton(
                    text=f'{dep_name}',
                    callback_data=EventDepartment(
                        event_depart=dep_id).pack())
            ]
        )
    departments_buttons.append(
        [
            InlineKeyboardButton(
                text=AdminMenuActions.BACK.value,
                callback_data=AdminMenuActionsCD(
                    admen_act=AdminMenuActions.BACK).pack())
        ]
    )
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=departments_buttons)


async def subdivision_keydoard():
    db = Database()
    subdivisions_buttons = []
    for subdiv_id, subdiv_name in await db.select_subdivisions():
        subdivisions_buttons.append(
            [
                InlineKeyboardButton(
                    text=f'{subdiv_name}',
                    callback_data=EventSubdivision(
                        event_subdiv=subdiv_id).pack())
            ]
        )
    subdivisions_buttons.append(
        [
            InlineKeyboardButton(
                text=AdminMenuActions.BACK.value,
                callback_data=AdminMenuActionsCD(
                    admen_act=AdminMenuActions.BACK).pack())
        ]
    )
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=subdivisions_buttons)
