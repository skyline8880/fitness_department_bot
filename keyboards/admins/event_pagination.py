

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.message.admins.events import comming_events_list, events_to_send_list
from database.database import Database
from filters.callback_filters import AdminMenuActions, AdminMenuActionsCD


class GetCurrentEventCD(CallbackData, prefix='event_id'):
    event_id: int


class EventPageRangeCD(CallbackData, prefix='page_range'):
    event_category: str
    page: int
    max_pages: int


class CurrentPageRangeCD(CallbackData, prefix='page_choice'):
    event_category: str
    page: int


class NavigationCD(CallbackData, prefix='move_to'):
    event_category: str
    page: int


class Paginator():
    def __init__(self, event_category='comming', page=1, max_pages=None):
        self.event_category = event_category
        self.event_list = None
        self.page = page
        self.max_pages = max_pages

    async def create_list(self):
        db = Database()
        METHODS = {
            'comming': [
                db.select_comming_events, comming_events_list],
            'to_send': [
                db.select_comming_events_by_sent_status, events_to_send_list],
        }
        self.event_list = await METHODS[self.event_category][0]()
        if self.event_list == []:
            return None, None
        event_count = len(self.event_list)
        start = self.page * 5 - 5
        end = start + 5
        if event_count < end:
            end = event_count + 1
        page_count = event_count // 5
        if event_count // 5 < event_count / 5:
            page_count = event_count // 5 + 1
        if self.max_pages is None:
            self.max_pages = page_count
        event_list_buttons = []
        # for event_id, name in self.event_list[start:end]:
        for (
            event_id,
            _,  # telegram_id,
            _,  # department_id,
            _,  # subdivision_id,
            _,  # event_date,
            name,
            _,  # description,
            _,  # is_free,
            _,  # is_active,
            _,  # sent,
            _,  # photo_id
            _   # executor
        ) in self.event_list[start:end]:
            event_list_buttons.append(
                [
                    InlineKeyboardButton(
                        text=f'№: {event_id} - {name}',
                        callback_data=GetCurrentEventCD(
                            event_id=event_id
                        ).pack()
                    )
                ]
            )
        if page_count > 1:
            event_list_buttons.append(
                self.navigation())
        event_list_buttons.append(
            [
                InlineKeyboardButton(
                    text=AdminMenuActions.BACK.value,
                    callback_data=AdminMenuActionsCD(
                        admen_act=AdminMenuActions.BACK).pack())
            ]
        )
        return (InlineKeyboardMarkup(
            row_width=3, inline_keyboard=event_list_buttons),
            METHODS[self.event_category][1]())

    def navigation(self):
        next = '▶'
        previous = '◀'
        navigation_buttons = []
        if self.page == 1 and self.max_pages == 1:
            navigation_buttons.append(
                InlineKeyboardButton(
                    text=f'{self.page}/{self.max_pages}',
                    callback_data=EventPageRangeCD(
                        event_category=self.event_category,
                        page=self.page,
                        max_pages=self.max_pages).pack()))
        elif self.page == 1 and self.max_pages > 1:
            navigation_buttons.append(InlineKeyboardButton(
                text=f'{self.page}/{self.max_pages}',
                callback_data=EventPageRangeCD(
                    event_category=self.event_category,
                    page=self.page,
                    max_pages=self.max_pages).pack()))
            navigation_buttons.append(InlineKeyboardButton(
                text=next,
                callback_data=NavigationCD(
                    event_category=self.event_category,
                    page=self.page + 1).pack()))
        elif self.page > 1 and self.max_pages > self.page:
            navigation_buttons.append(InlineKeyboardButton(
                text=previous,
                callback_data=NavigationCD(
                    event_category=self.event_category,
                    page=self.page - 1).pack()))
            navigation_buttons.append(InlineKeyboardButton(
                text=f'{self.page}/{self.max_pages}',
                callback_data=EventPageRangeCD(
                    event_category=self.event_category,
                    page=self.page,
                    max_pages=self.max_pages).pack()))
            navigation_buttons.append(InlineKeyboardButton(
                text=next,
                callback_data=NavigationCD(
                    event_category=self.event_category,
                    page=self.page + 1).pack()))
        elif self.page > 1 and self.max_pages == self.page:
            navigation_buttons.append(InlineKeyboardButton(
                text=previous,
                callback_data=NavigationCD(
                    event_category=self.event_category,
                    page=self.page - 1).pack()))
            navigation_buttons.append(InlineKeyboardButton(
                text=f'{self.page}/{self.max_pages}',
                callback_data=EventPageRangeCD(
                    event_category=self.event_category,
                    page=self.page,
                    max_pages=self.max_pages).pack()))
        return navigation_buttons

    async def page_range(self):
        buttons = []
        row = []
        for page in range(self.page, self.max_pages + 1):
            row.append(
                InlineKeyboardButton(
                    text=f'{page}',
                    callback_data=CurrentPageRangeCD(
                        event_category=self.event_category,
                        page=page
                    ).pack()
                )
            )
            if row == 6:
                buttons.append(row)
                row = []
        if row not in buttons:
            buttons.append(row)
        return InlineKeyboardMarkup(
            row_width=6, inline_keyboard=buttons)
