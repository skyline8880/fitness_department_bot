from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.database import Database
from filters.callback_filters import (AdminMenuActions, AdminMenuActionsCD,
                                      CurrenEventActionsCD,
                                      CurrentEventActions,
                                      CustomerEventActionsCD, EventFreeActions,
                                      EventPayment, EventsActions,
                                      EventsActionsCD,
                                      SkipPhotoCD, SkipPhoto)


def events_keydoard():
    buttons = []
    for butt in EventsActions:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=butt.value,
                    callback_data=EventsActionsCD(
                        event_act=butt).pack())
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


def back_button(expecting_photo: bool = False):
    buttons = [
        [
            InlineKeyboardButton(
                text=AdminMenuActions.BACK.value,
                callback_data=AdminMenuActionsCD(
                    admen_act=AdminMenuActions.BACK).pack())
        ]
    ]
    if expecting_photo:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=SkipPhoto.NOPHOTO.value,
                    callback_data=SkipPhotoCD(
                        admen_act=SkipPhoto.NOPHOTO).pack())
            ]            
        )
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=buttons)


def free_type_keyboard():
    buttons = [
        [
            InlineKeyboardButton(
                text=EventFreeActions.PAY.value,
                callback_data=EventPayment(
                    isfree=0,
                    name=EventFreeActions.PAY).pack())
        ],
        [
            InlineKeyboardButton(
                text=EventFreeActions.FREE.value,
                callback_data=EventPayment(
                    isfree=1,
                    name=EventFreeActions.FREE).pack())
        ],
        [
            InlineKeyboardButton(
                text=AdminMenuActions.BACK.value,
                callback_data=AdminMenuActionsCD(
                    admen_act=AdminMenuActions.BACK).pack())
        ]
    ]
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=buttons)


def current_event_keyboard(event_data):
    (
        event_id,
        event_date,
        creator_id,
        creator_lname,
        creator_fname,
        creator_phone,
        department_id,
        department,
        subdivision_id,
        subdivision,
        event_name,
        event_description,
        event_isfree,
        event_isactive,
        event_sent
    ) = event_data
    buttons = []
    if not event_sent:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=CurrentEventActions.SEND.value,
                    callback_data=CurrenEventActionsCD(
                        curev_act=CurrentEventActions.SEND).pack())
            ]
        )
    activate_action = InlineKeyboardButton(
            text=CurrentEventActions.ACTIVATE.value,
            callback_data=CurrenEventActionsCD(
                curev_act=CurrentEventActions.ACTIVATE).pack())
    if event_isactive:
        activate_action = InlineKeyboardButton(
                text=CurrentEventActions.DELETE.value,
                callback_data=CurrenEventActionsCD(
                    curev_act=CurrentEventActions.DELETE).pack())
    buttons.append(
            [
                InlineKeyboardButton(
                    text=CurrentEventActions.STATS.value,
                    callback_data=CurrenEventActionsCD(
                        curev_act=CurrentEventActions.STATS).pack()),
                activate_action
            ],
    )
    buttons.append(
        [
            InlineKeyboardButton(
                text=AdminMenuActions.BACK.value,
                callback_data=AdminMenuActionsCD(
                    admen_act=AdminMenuActions.BACK).pack())
        ]
    )
    return InlineKeyboardMarkup(
        row_width=2, inline_keyboard=buttons)


async def customer_event_keyboard(event_id, customer_id):
    db = Database()
    customer_enroll_data = await db.select_current_customer_enroll(
        event_id=event_id,
        customer_id=customer_id)
    actions = await db.select_customer_enroll_actions()
    buttons = []
    for act_id, act_name in actions:
        stat = '⬜️'
        if customer_enroll_data is not None:
            if act_id == customer_enroll_data[0]:
                stat = '🔳'
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f'{stat} {act_name}',
                    callback_data=CustomerEventActionsCD(
                        act_id=act_id,
                        custom_act=act_name).pack())
            ]
        )
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=buttons)
