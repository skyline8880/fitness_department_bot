from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.database import Database
from filters.callback_filters import DepartmentsCD, ReferencesCD
from keyboards.admins.admins_menu import menu_button
from keyboards.menu_keyboard import to_menu_button, to_subdivs_button


async def department_keydoard(telegram_id, is_admin=False, is_welcome=False):
    db = Database()
    users_department_data = await db.select_user_departments_by_sign(
        telegram_id=telegram_id)
    department_buttons = []
    for dep_id, dep_name, status in users_department_data:
        check = '🔳'
        is_checked = 1
        if status is None:
            check = '⬜️'
            is_checked = 0
        department_buttons.append(
            [
                InlineKeyboardButton(
                    text=f'{check} {dep_name}',
                    callback_data=DepartmentsCD(
                        depart=dep_id,
                        is_checked=is_checked).pack())
            ]
        )
    if is_welcome:
        department_buttons.append(to_subdivs_button)
    else:
        if is_admin:
            department_buttons.append(menu_button)
        else:
            department_buttons.append(to_menu_button)
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=department_buttons)


async def subdivision_keydoard(telegram_id, is_admin=False):
    db = Database()
    users_reference_data = await db.select_user_references_by_sign(
        telegram_id=telegram_id)
    references_buttons = []
    for sub_id, sub_name, status in users_reference_data:
        check = '🔳'
        is_checked = 1
        if status is None:
            check = '⬜️'
            is_checked = 0
        references_buttons.append(
            [
                InlineKeyboardButton(
                    text=f'{check} {sub_name}',
                    callback_data=ReferencesCD(
                        subdiv=sub_id,
                        is_checked=is_checked).pack())
            ]
        )
    if is_admin:
        references_buttons.append(menu_button)
    else:
        references_buttons.append(to_menu_button)
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=references_buttons)
