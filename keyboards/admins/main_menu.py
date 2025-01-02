from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters.callback_filters import AdminMenu, AdminMenuCD
from keyboards.menu_keyboard import club_menu_button, subdiv_menu_button


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
    buttons.append(club_menu_button)
    buttons.append(subdiv_menu_button)
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=buttons)
