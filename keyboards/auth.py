from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

from constants.actions import Action
from filters.callback_filters import ActionsCD

get_contact_button = KeyboardButton(
    text='Отправить контакт', request_contact=True)
get_contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[[get_contact_button]],
    resize_keyboard=True,
    one_time_keyboard=True)

remove_conact_keyboard = ReplyKeyboardRemove()


def cancel_keyboard():
    button = [
        InlineKeyboardButton(
            text=Action.CANCEL.value,
            callback_data=ActionsCD(
                action=Action.CANCEL).pack())
    ]
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=[button])


def cancel_and_skip_keyboard():
    buttons = [
        [
            InlineKeyboardButton(
                text=Action.CANCEL.value,
                callback_data=ActionsCD(
                    action=Action.CANCEL).pack()),
            InlineKeyboardButton(
                text=Action.SKIP.value,
                callback_data=ActionsCD(
                    action=Action.SKIP).pack())
        ]
    ]
    return InlineKeyboardMarkup(
        row_width=2, inline_keyboard=buttons)
