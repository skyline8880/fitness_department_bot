from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters.callback_filters import Menu, MenuCD

club_menu_button = [
    InlineKeyboardButton(
        text=Menu.CLUB.value,
        callback_data=MenuCD(
            menu_act=Menu.CLUB).pack())
]
subdiv_menu_button = [
    InlineKeyboardButton(
        text=Menu.SUBDIV.value,
        callback_data=MenuCD(
            menu_act=Menu.SUBDIV).pack())
]


def menu_keyboard():
    menu_buttons = [club_menu_button, subdiv_menu_button]
    return InlineKeyboardMarkup(
        row_width=2, inline_keyboard=menu_buttons)
