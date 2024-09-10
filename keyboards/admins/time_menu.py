from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters.callback_filters import AdminMenuActions, AdminMenuActionsCD


class TimeHour(CallbackData, prefix='hour'):
    year: int
    month: int
    day: int
    hour: int


class TimeMinute(CallbackData, prefix='minute'):
    year: int
    month: int
    day: int
    hour: int
    minute: int


class Hour():
    def __call__(self, **kwargs):
        year = kwargs['year']
        month = kwargs['month']
        day = kwargs['day']
        back_button = [
            InlineKeyboardButton(
                text=AdminMenuActions.BACK.value,
                callback_data=AdminMenuActionsCD(
                    admen_act=AdminMenuActions.BACK).pack())
        ]
        result = []
        row = []
        for hour in range(25):
            row.append(
                InlineKeyboardButton(
                    text=f'{hour:02d}',
                    callback_data=TimeHour(
                        year=year,
                        month=month,
                        day=day,
                        hour=hour).pack()))
            if len(row) == 4:
                result.append(row)
                row = []
        result.append(back_button)
        return InlineKeyboardMarkup(
            row_width=4,
            inline_keyboard=result)


class Minute():
    def __call__(self, **kwargs):
        year = kwargs['year']
        month = kwargs['month']
        day = kwargs['day']
        hour = kwargs['hour']
        back_button = [
            InlineKeyboardButton(
                text=AdminMenuActions.BACK.value,
                callback_data=AdminMenuActionsCD(
                    admen_act=AdminMenuActions.BACK).pack())
        ]
        result = []
        for minute in range(0, 60, 15):
            result.append(
                InlineKeyboardButton(
                    text=f'{minute:02d}',
                    callback_data=TimeMinute(
                        year=year,
                        month=month,
                        day=day,
                        hour=hour,
                        minute=minute).pack()))

        return InlineKeyboardMarkup(
            row_width=4,
            inline_keyboard=[result, back_button])


HourPicker = Hour()
MinutePicker = Minute()
