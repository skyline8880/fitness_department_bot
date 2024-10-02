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

    def range_options(self, r_type: str, button: int):
        add = self.date + relativedelta(years=1)
        take = self.date - relativedelta(years=1)
        if r_type == 'month':
            add = self.date + relativedelta(months=1)
            take = self.date - relativedelta(months=1)
        return [
            InlineKeyboardButton(
                text=f'{self.previous}',
                callback_data=DateMove(
                    year=take.year,
                    month=take.month,
                    day=take.day).pack()),
            InlineKeyboardButton(
                text=f'{button}',
                callback_data=OpenRange(
                    year=self.year,
                    month=self.month,
                    day=self.day,
                    r_type=r_type).pack()),
            InlineKeyboardButton(
                text=f'{self.next}',
                    callback_data=DateMove(
                        year=add.year,
                        month=add.month,
                        day=add.day).pack()),
        ]


def week_range(self):
    weeks_buttons = []
    
    for weekday in range(7):
        date = self.today + datetime.timedelta(days=(weekday - self.today.weekday()))

        text = date.strftime("%a")
        callback_data = WeekInfo(week=text).pack()

        # Создаем InlineKeyboardButton
        button = InlineKeyboardButton(text=text, callback_data=callback_data)

        # Добавляем созданный объект кнопки в список weeks_buttons
        weeks_buttons.append(button)

        # Проверка наличия атрибута text у объекта кнопки
        if hasattr(button, 'text'):
            print("У объекта есть доступный атрибут 'text'")
        else:
            print("У объекта нет доступного атрибута 'text'")

    return weeks_buttons
"""
    def week_range(self):
        weeks_buttons = []
        for weekday in range(7):
            date = self.today + datetime.timedelta(days=(weekday - self.today.weekday()))
            weeks_buttons.append(
                InlineKeyboardButton(
                    text=f'{date.strftime("%a")}',
                    callback_data=WeekInfo(week=date.strftime("%a")).pack())
            )
        return weeks_buttons
"""
def days_range(self):
        result = []
        days_data = calendar.monthcalendar(year=self.year, month=self.month)
        for week in days_data:
            weeks_days = []
            for day in week:
                name = day
                if day == 0:
                    name = ' '
                weeks_days.append(
                    InlineKeyboardButton(
                        text=f'{name}',
                        callback_data=DatePick(
                            year=self.year,
                            month=self.month,
                            day=day).pack()))
            result.append(weeks_days)
        return result
"""
class UserDatePicker():
    def __init__(self) -> None:
        self.next = '▶'
        self.previous = '◀'
        self.weeks = calendar.weekheader(width=2)
        self.year = None
        self.month = None
        self.day = None
        self.date = None
        self.month_name = None
        self.back_button = []

    def range_options(self, r_type: str, button: Union[str, int]):
        add = self.date + relativedelta(years=1)
        take = self.date - relativedelta(years=1)
        if r_type == 'month':
            add = self.date + relativedelta(months=1)
            take = self.date - relativedelta(months=1)
        return [
            InlineKeyboardButton(
                text=f'{self.previous}',
                callback_data=DateMove(
                    year=take.year,
                    month=take.month,
                    day=take.day).pack()),
            InlineKeyboardButton(
                text=f'{button}',
                callback_data=OpenRange(
                    year=self.year,
                    month=self.month,
                    day=self.day,
                    r_type=r_type).pack()),
            InlineKeyboardButton(
                text=f'{self.next}',
                callback_data=DateMove(
                    year=add.year,
                    month=add.month,
                    day=add.day).pack()),
        ]

    def week_range(self):
        weeks_buttons = []
        for week in self.weeks.split():
            weeks_buttons.append(
                InlineKeyboardButton(
                    text=f'{week}',
                    callback_data=WeekInfo(
                        week=week).pack())
            )
        return weeks_buttons

    def days_range(self):
        result = []
        days_data = calendar.monthcalendar(year=self.year, month=self.month)
        for week in days_data:
            weeks_days = []
            for day in week:
                name = day
                if day == 0:
                    name = '󠀠 '
                weeks_days.append(
                    InlineKeyboardButton(
                        text=f'{name}',
                        callback_data=DatePick(
                            year=self.year,
                            month=self.month,
                            day=day).pack()))
            result.append(weeks_days)
        return result
"""
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