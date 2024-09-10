from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters.callback_filters import Menu, MenuCD


def menu_keyboard():
    menu_buttons = [
        [
            InlineKeyboardButton(
                text=Menu.CLUB.value,
                callback_data=MenuCD(
                    menu_act=Menu.CLUB).pack())
        ],
        [
            InlineKeyboardButton(
                text=Menu.SUBDIV.value,
                callback_data=MenuCD(
                    menu_act=Menu.SUBDIV).pack())
        ],
    ]
    return InlineKeyboardMarkup(
        row_width=2, inline_keyboard=menu_buttons)
