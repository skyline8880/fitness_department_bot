from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters.callback_filters import AdminMenu, AdminMenuCD


def admin_keydoard():
    buttons = []
    for butt in AdminMenu:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=butt.value,
                    callback_data=AdminMenuCD(
                        adm_menu=butt).pack())
            ]
        )
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=buttons)
