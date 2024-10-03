import calendar
import datetime
from dateutil import parser
from dateutil.parser import parse
import datetime as dt
from typing import Union

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dateutil.relativedelta import relativedelta

from filters.callback_filters import AdminMenuActions, AdminMenuActionsCD


class OpenRange(CallbackData, prefix='range'):
    year: int
    month: int
    day: int
    r_type: str


class ScrollRange(CallbackData, prefix='scroll_range'):
    year: int
    month: int
    day: int
    r_type: str


class WeekInfo(CallbackData, prefix='week'):
    week: str


class DateMove(CallbackData, prefix='date_move'):
    year: int
    month: int
    day: int


class DatePick(CallbackData, prefix='date_pick'):
    year: int
    month: int
    day: int



class UserDatePicker():
    def __init__(self) -> None:
        self.next = '▶️'
        self.previous = '◀️'
        self.today = datetime.datetime.today()
        self.year = self.today.year
        self.month = self.today.month
        self.day = self.today.day
        self.date = datetime.datetime(self.year, self.month, self.day)

    def range_options(self, r_type: str, button: str):
        add = self.date + relativedelta(years=1) if r_type == 'year' else self.date + relativedelta(months=1)
        take = self.date - relativedelta(years=1) if r_type == 'year' else self.date - relativedelta(months=1)

        month_translations = {
            'jan': 'янв',
            'feb': 'фев',
            'mar': 'мар',
            'apr': 'апр',
            'may': 'май',
            'jun': 'июн',
            'jul': 'июл',
            'aug': 'авг',
            'sep': 'сен',
            'oct': 'окт',
            'nov': 'ноя',
            'dec': 'дек'
        }

        return [
            InlineKeyboardButton(
                text=f'{self.previous}',
                callback_data=f'{take.year}-{month_translations[take.strftime("%b").lower()]}-{take.day}'
            ),
            InlineKeyboardButton(
                text=button,
                callback_data=f'{self.year}-{self.month}-{self.day}'
            ),
            InlineKeyboardButton(
                text=f'{self.next}',
                callback_data=f'{add.year}-{month_translations[add.strftime("%b").lower()]}-{add.day}'
            )
        ]


    def week_range(self):
        weeks_buttons = []
        
        for i in range(7):
            day = self.today + datetime.timedelta(days=(i - self.today.weekday()))
            
            text = day.strftime('%a')  # Получаем сокращенное название дня недели на английском
            day_name_ru = {
                'Mon': 'Пн',
                'Tue': 'Вт',
                'Wed': 'Ср',
                'Thu': 'Чт',
                'Fri': 'Пт',
                'Sat': 'Сб',
                'Sun': 'Вс'
            }
            text_ru = day_name_ru.get(text)

            callback_data = f"week-{text}"
            
            # Создаем InlineKeyboardButton
            button = InlineKeyboardButton(text=text_ru, callback_data=callback_data)
            
            weeks_buttons.append(button)

        return weeks_buttons

    def days_range(self):
        result = []
        days_data = [
            [day if day != 0 else '' for day in week]
            for week in calendar.monthcalendar(self.year, self.month)
        ]
        for week in days_data:
            weeks_days = []
            for day in week:
                if day:
                    day = datetime.datetime(self.year, self.month, day)
                    text = day.strftime('%a')  # Получаем сокращенное название дня недели на русском
                    callback_data = f"{self.year}-{self.month}-{day.day}"
                    weeks_days.append(
                        InlineKeyboardButton(
                            text=text,
                            callback_data=callback_data
                        )
                    )
                else:
                    weeks_days.append(
                        InlineKeyboardButton(
                            text='',
                            callback_data=''
                        )
                    )
            result.append(weeks_days)
        return result
    def __call__(
            self,
            year: int = None,
            month: int = None,
            day: int = None) -> InlineKeyboardMarkup:
        if year is None:
            now = dt.datetime.now()
            year = now.year
            month = now.month
            day = now.day
        self.date = dt.date(year=year, month=month, day=day)
        self.year = self.date.year
        self.month = self.date.month
        self.day = self.date.day
        self.month_name = str(dt.date.strftime(self.date, '%B'))
        self.back_button = [
            InlineKeyboardButton(
                text=AdminMenuActions.BACK.value,
                callback_data=AdminMenuActionsCD(
                    admen_act=AdminMenuActions.BACK).pack())
        ]
        return InlineKeyboardMarkup(
            row_width=7,
            inline_keyboard=[
                self.range_options(r_type='year', button=self.year),
                self.range_options(r_type='month', button=self.month_name),
                self.week_range(),
                *self.days_range(),
                self.back_button
            ])


class Range():
    def __init__(self) -> None:
        self.next = '▶'
        self.previous = '◀'
        self.year = None
        self.month = None
        self.day = None
        self.back_button = []

    def __call__(self, r_type, **kwargs):
        delta = 6
        self.year = kwargs['year']
        self.month = kwargs['month']
        self.day = kwargs['day']
        self.back_button = [
            InlineKeyboardButton(
                text=AdminMenuActions.BACK.value,
                callback_data=AdminMenuActionsCD(
                    admen_act=AdminMenuActions.BACK).pack())
        ]
        result = []
        row = []
        if r_type == 'year':
            for n in range(self.year - delta, self.year + delta):
                row.append(
                    InlineKeyboardButton(
                        text=f'{n}',
                        callback_data=DateMove(
                            year=n,
                            month=self.month,
                            day=self.day).pack()),
                )
                if len(row) == 4:
                    result.append(row)
                    row = []
            result.append(
                [
                    InlineKeyboardButton(
                        text=f'{self.previous}',
                        callback_data=ScrollRange(
                            year=self.year - delta,
                            month=self.month,
                            day=self.day,
                            r_type=r_type).pack()),
                    InlineKeyboardButton(
                        text=f'{self.next}',
                        callback_data=ScrollRange(
                            year=self.year + delta,
                            month=self.month,
                            day=self.day,
                            r_type=r_type).pack()),
                ]
            )
            result.append(self.back_button)
            return InlineKeyboardMarkup(
                row_width=4,
                inline_keyboard=result)
        for n in range(1, 13):
            month = str(
                dt.date.strftime(
                    dt.date(year=self.year, month=n, day=self.day), '%B'))
            row.append(
                InlineKeyboardButton(
                    text=month,
                    callback_data=DateMove(
                        year=self.year,
                        month=n,
                        day=self.day).pack()),
            )
            if len(row) == 4:
                result.append(row)
                row = []
        result.append(self.back_button)
        return InlineKeyboardMarkup(
                row_width=4,
                inline_keyboard=result)


DateRange = Range()
DatePicker = UserDatePicker()