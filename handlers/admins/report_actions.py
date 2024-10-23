import re
from datetime import datetime

from aiogram import F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.chat_action import ChatActionSender
from dateutil.relativedelta import relativedelta

from bot.bot import bot
from bot.message.admins.reports import (add_reports_period_message,
                                        period_reports_data,
                                        period_reports_nodata)
from database.database import Database
from filters.callback_filters import (DateReports, DateReportsCD,
                                      ReportsActions, ReportsActionsCD)
from filters.filters import IsAdmin, IsPrivate
from keyboards.admins.reports_menu import (back_to_reports,
                                           date_reports_keyboard)
from state.state import DatePeriod

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
            filepath, filename = await db.subscribers(result)
            await bot.send_document(
                chat_id=query.message.chat.id,
                document=FSInputFile(path=filepath, filename=filename),
                caption='Отчет по пользователям готов'
                )
        return

    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        text=action,
        reply_markup=date_reports_keyboard())


@router.callback_query(DateReportsCD.filter(), IsPrivate(), IsAdmin())
async def choose_reports_period_callback(
        query: CallbackQuery, state: FSMContext) -> None:

    action = query.data.split(':')[-1]
    await query.answer(action)
    reports_action = query.message.text
    await state.set_state(DatePeriod.action)
    await state.update_data(action=reports_action)

    db = Database()
    action_sender = ChatActionSender(
            bot=bot,
            chat_id=query.from_user.id,
            action=ChatAction.UPLOAD_DOCUMENT
        )
    async with action_sender:
        if action == DateReports.CURRENT.value:
            current_date = datetime.now().date()
            begin_current_month = datetime(
                year=current_date.year,
                month=current_date.month,
                day=1).date()
            end_current_month = (
                begin_current_month + relativedelta(months=1, days=-1))
            print(begin_current_month, end_current_month)
            result = await db.select_group_events_query(
                begin_current_month, end_current_month)
            if not result:
                await bot.send_message(chat_id=query.message.chat.id,
                                       text=period_reports_nodata(
                                           begin_current_month,
                                           end_current_month))
            else :
                filepath, filename = await db.fetchdata(
                    result, begin_current_month, end_current_month)
            await bot.send_document(
                chat_id=query.message.chat.id,
                document=FSInputFile(path=filepath, filename=filename),
                caption='Отчет за текущий месяц готов'
            )
            return
        elif action == DateReports.PREVIOUS.value:
            current_date = datetime.now().date()
            first_day_of_month = datetime(
                year=current_date.year,
                month=current_date.month,
                day=1).date()
            end_previous_month = first_day_of_month - relativedelta(days=1)
            begin_previous_month = first_day_of_month - relativedelta(months=1)
            print(first_day_of_month, begin_previous_month, end_previous_month)
            result = await db.select_group_events_query(
                begin_previous_month, end_previous_month)
            if not result:
                await bot.send_message(chat_id=query.message.chat.id,
                                       text=period_reports_nodata(
                                           begin_previous_month,
                                           end_previous_month))
            else :
                filepath, filename = await db.fetchdata(
                    result, begin_previous_month, end_previous_month)
            await bot.send_document(
                    chat_id=query.message.chat.id,
                    document=FSInputFile(path=filepath, filename=filename),
                    caption='Отчет за предыдущий месяц готов'
                )
            return
        await state.set_state(DatePeriod.start_message)
        await state.update_data(start_message=query.message.message_id)
        await state.set_state(DatePeriod.period)
        await bot.edit_message_text(
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            text=add_reports_period_message(),
            reply_markup=back_to_reports())


@router.message(DatePeriod.period,
                IsPrivate(),
                IsAdmin()
                )
async def choose_reports_period_message(
        message: Message, state: FSMContext) -> None:
    try:
        cleaned_input = re.sub(r'\s*-\s*', '-', message.text)
        if not re.match(
                r'^\s*\d{2}\.\d{2}\.\d{4}\s*-\s*\d{2}\.\d{2}\.\d{4}\s*$',
                message.text):
            await bot.delete_message(chat_id=message.chat.id,
                                     message_id=message.message_id)
            await bot.send_message(chat_id=message.chat.id,
                                   text=add_reports_period_message())
            return
        start, end = cleaned_input.split('-')
        start_date = datetime.strptime(
            start, '%d.%m.%Y').strftime('%Y-%m-%d')
        end_date = datetime.strptime(
            end, '%d.%m.%Y').strftime('%Y-%m-%d')
        db = Database()
        result = await db.select_group_events_query(start_date, end_date)
        if not result:
            await bot.send_message(chat_id=message.chat.id,
                                   text=period_reports_nodata(start, end))
            return
        filepath, filename = await db.fetchdata(result, start_date, end_date)
        await bot.send_document(
            chat_id=message.chat.id,
            document=FSInputFile(path=filepath, filename=filename),
            caption=period_reports_data(start, end)
            )
        data = await state.get_data()
        start_message = int(data["start_message"])
        action = data["action"]
        await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=start_message,
            text=action,
            reply_markup=date_reports_keyboard()
        )
        await state.clear()
    except ValueError:
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id)
        await bot.send_message(chat_id=message.chat.id,
                               text=add_reports_period_message())
