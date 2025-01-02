from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.database import Database
from filters.callback_filters import ActionsCD, DepartmentsCD, ReferencesCD
from keyboards.admins.admins_menu import menu_button


async def department_keydoard(telegram_id, welcome=None):
    db = Database()
    users_department_data = await db.select_user_departments_by_sign(
        telegram_id=telegram_id)
    is_admin = await db.select_user_by_sign(telegram_id)
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
    if is_admin[1]:
        department_buttons.append(menu_button)
        return InlineKeyboardMarkup(
            row_width=1, inline_keyboard=department_buttons)
    if welcome is not None:
        for button in welcome:
            department_buttons.append(
                [
                    InlineKeyboardButton(
                        text=button.value,
                        callback_data=ActionsCD(
                            action=button).pack())
                ]
            )
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=department_buttons)


async def subdivision_keydoard(telegram_id, welcome=None):
    db = Database()
    users_reference_data = await db.select_user_references_by_sign(
        telegram_id=telegram_id)
    is_admin = await db.select_user_by_sign(telegram_id)
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
    if is_admin[1]:
        references_buttons.append(menu_button)
        return InlineKeyboardMarkup(
            row_width=1, inline_keyboard=references_buttons)
    if welcome is not None:
        for button in welcome:
            references_buttons.append(
                [
                    InlineKeyboardButton(
                        text=button.value,
                        callback_data=ActionsCD(
                            action=button).pack())
                ]
            )
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=references_buttons)
