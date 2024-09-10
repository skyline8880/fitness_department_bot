from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters.callback_filters import (AdminMenuActions, AdminMenuActionsCD,
                                      ReportsActions, ReportsActionsCD)


def reports_keydoard():
    buttons = []
    for butt in ReportsActions:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=butt.value,
                    callback_data=ReportsActionsCD(
                        report_act=butt).pack())
            ]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text=AdminMenuActions.TOMENU.value,
                callback_data=AdminMenuActionsCD(
                    admen_act=AdminMenuActions.TOMENU).pack())
        ]
    )
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=buttons)
