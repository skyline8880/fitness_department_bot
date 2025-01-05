from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from constants.actions import Action
from filters.callback_filters import ActionsCD, Menu, MenuCD

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
to_subdivs_button = [
    InlineKeyboardButton(
        text=Action.TOSUBDIVS.value,
        callback_data=ActionsCD(
            action=Action.TOSUBDIVS).pack())
]
to_menu_button = [
    InlineKeyboardButton(
        text=Action.TOMENU.value,
        callback_data=ActionsCD(
            action=Action.TOMENU).pack())
]


def menu_keyboard():
    menu_buttons = [club_menu_button, subdiv_menu_button]
    return InlineKeyboardMarkup(
        row_width=2, inline_keyboard=menu_buttons)
