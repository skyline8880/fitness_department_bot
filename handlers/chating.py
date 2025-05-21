from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.bot import bot
from filters.filters import IsAdmin, IsAuth, IsGroup

router = Router()


@router.message(IsAuth(), IsGroup(), ~IsAdmin())
async def cautch_unauth_member(message: Message, state: FSMContext) -> None:
    try:
        await bot.ban_chat_member(
            chat_id=await bot.get_group_id(),
            user_id=message.from_user.id)
    except Exception as e:
        print(f'error ban user: {e}')


@router.message(IsAuth())
async def send_any_message(message: Message, state: FSMContext) -> None:
    await bot.chating(message=message)
