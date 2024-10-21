from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters.callback_filters import (AdminMenu, AdminMenuActions,
                                      AdminMenuActionsCD, AdminMenuCD,
                                      DateReports, DateReportsCD,
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


def date_reports_keyboard():
    buttons = []
    for butt in DateReports:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=butt.value,
                    callback_data=DateReportsCD(
                        date_report=butt).pack())
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


def back_to_reports():
    menu_button = [
        InlineKeyboardButton(
            text=AdminMenu.REPORTS.value,
            callback_data=AdminMenuCD(
                adm_menu=AdminMenu.REPORTS).pack())
    ]
    return InlineKeyboardMarkup(
        row_width=2, inline_keyboard=[menu_button])
