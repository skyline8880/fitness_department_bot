from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters.callback_filters import (AdminMenuActions, AdminMenuActionsCD,
                                      AdminsActions, AdminsActionsCD)

menu_button = [
    InlineKeyboardButton(
        text=AdminMenuActions.TOMENU.value,
        callback_data=AdminMenuActionsCD(
            admen_act=AdminMenuActions.TOMENU).pack())
]


def admins_keydoard():
    buttons = []
    for butt in AdminsActions:
        buttons.append(
            InlineKeyboardButton(
                text=butt.value,
                callback_data=AdminsActionsCD(
                    adm_act=butt).pack())
        )
    return InlineKeyboardMarkup(
        row_width=2, inline_keyboard=[buttons, menu_button])


def back_to_admins():
    menu_button = [
        InlineKeyboardButton(
            text=AdminMenuActions.ADMINS.value,
            callback_data=AdminMenuActionsCD(
                admen_act=AdminMenuActions.ADMINS).pack())
    ]
    return InlineKeyboardMarkup(
        row_width=2, inline_keyboard=[menu_button])
