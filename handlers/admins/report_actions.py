from aiogram import F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.utils.chat_action import ChatActionSender

from bot.bot import bot
from database.database import Database
from filters.callback_filters import (DateReportsCD, ReportsActions,
                                      ReportsActionsCD)
from filters.filters import IsAdmin, IsPrivate
from keyboards.admins.reports_menu import date_reports_keyboard

router = Router()


@router.callback_query(
        ReportsActionsCD.filter(F.report_act.in_({
            ReportsActions.EVENTS, ReportsActions.USERS})),
        IsPrivate(),
        IsAdmin())
async def reports_actions(
        query: CallbackQuery, state: FSMContext) -> None:
    action = query.data.split(':')[-1]
    await query.answer(action)
    db = Database()
    if action == ReportsActions.USERS.value:
        action_sender = ChatActionSender(
            bot=bot,
            chat_id=query.from_user.id,
            action=ChatAction.UPLOAD_DOCUMENT
        )
        async with action_sender:
            result = await db.select_subscribers_query()
            filename = await db.subscribers(result)
            report_path = f'reports/{filename}'
            await bot.send_document(
                chat_id=query.message.chat.id,
                document=FSInputFile(path=report_path, filename=filename),
                caption='Текст для описания документа'
            )
        return
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        text=action,
        reply_markup=date_reports_keyboard(type_report=action))


@router.callback_query(
        DateReportsCD.filter(),
        IsPrivate(),
        IsAdmin())
async def choose_reports_period(
        query: CallbackQuery, state: FSMContext) -> None:
    print(query.data)
    await query.answer('test')
