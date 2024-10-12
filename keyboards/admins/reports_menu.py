from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters.callback_filters import (AdminMenuActions, AdminMenuActionsCD,
                                      ReportsActions, ReportsActionsCD)
import datetime

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


def events_reports_keyboard():
    
    buttons = []

    # Добавляем кнопку для текущего месяца
    current_month = datetime.datetime.now().strftime("%B")
    callback_data_current_month = f"event_date_report:current_month"
    button_current_month = InlineKeyboardButton(text="Текущий месяц", callback_data=callback_data_current_month)
    buttons.append([button_current_month])

    # Добавляем кнопку для предыдущего месяца
    previous_month = (datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().day)).strftime("%B")
    callback_data_previous_month = f"event_date_report:previous_month"
    button_previous_month = InlineKeyboardButton(text="Предыдущий месяц", callback_data=callback_data_previous_month)
    buttons.append([button_previous_month])

    # Добавляем кнопку для выбора диапазона дат
    callback_data_date_range = f"event_date_report:date_range"
    button_date_range = InlineKeyboardButton(text="Диапазон", callback_data=callback_data_date_range)
    buttons.append([button_date_range])

    # Добавляем кнопку для возврата в главное меню
    buttons.append([InlineKeyboardButton(text="To Menu", callback_data="to_menu")])
    
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=buttons)
