from typing import Union

from aiogram.enums.chat_type import ChatType
from aiogram.enums.content_type import ContentType
from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

from core.secrets import TelegramSectrets
from database.database import Database


class IsDev(Filter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        return message.from_user.id == TelegramSectrets.DEVELOPER


class IsAdmin(Filter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        db = Database()
        user_data = await db.select_user_by_sign(sign=message.from_user.id)
        if user_data is not None:
            return user_data[1]
        return False


class IsAuth(Filter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        db = Database()
        user_data = await db.select_user_by_sign(sign=message.from_user.id)
        if user_data is None:
            return False
        return True


class MessageIsValidContact(Filter):
    async def __call__(self, message: Message) -> bool:
        try:
            return message.contact.user_id == message.from_user.id
        except Exception:
            return False


class IsPrivate(Filter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        if isinstance(message, CallbackQuery):
            current_chat_type = message.message.chat.type
        else:
            current_chat_type = message.chat.type
        return current_chat_type == ChatType.PRIVATE.value


class IsGroup(Filter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        if isinstance(message, CallbackQuery):
            current_chat = message.message.chat
        else:
            current_chat = message.chat
        return current_chat.id == TelegramSectrets.GROUP_ID


class IsText(Filter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        return message.content_type == ContentType.TEXT.value


class IsPhoto(Filter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        return message.content_type == ContentType.PHOTO.value


class IsPhone(Filter):
    async def __call__(self, message: Message) -> bool:
        try:
            accum = ''
            for char in message.text:
                if isinstance(int(char), int):
                    accum += char
            return isinstance(int(accum), int)
        except Exception:
            return False
