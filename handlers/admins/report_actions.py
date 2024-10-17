from aiogram import F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery,
                           Message,
                           FSInputFile)
from aiogram.utils.chat_action import ChatActionSender
from bot.bot import bot
from database.database import Database
from filters.callback_filters import (DateReportsCD,
                                      DateReports,
                                      ReportsActions,
                                      ReportsActionsCD)
from filters.filters import IsAdmin, IsPrivate
from keyboards.admins.reports_menu import (date_reports_keyboard,
                                           back_to_reports)
from dateutil.relativedelta import relativedelta
from datetime import datetime
import re
from state.state import DatePeriod
from bot.message.admins.reports import add_reports_period_message

router = Router()


# Обработчик для действий с отчетами
@router.callback_query(
        ReportsActionsCD.filter(F.report_act.in_({
            ReportsActions.EVENTS, ReportsActions.USERS})),
        IsPrivate(),
        IsAdmin())
async def reports_actions(
        query: CallbackQuery, state: FSMContext) -> None:

    # Получаем действие из данных callback'а
    action = query.data.split(':')[-1]
    await query.answer(action)

    # Инициализируем подключение к базе данных
    db = Database()

    # Если выбрано действие с пользователями
    if action == ReportsActions.USERS.value:
        action_sender = ChatActionSender(
            bot=bot,
            chat_id=query.from_user.id,
            action=ChatAction.UPLOAD_DOCUMENT
        )
        # Выгружаем отчет и отправляем сообщение
        async with action_sender:
            result = await db.select_subscribers_query()
            filepath, filename = await db.subscribers(result)

            # Отправляем файл и сообщение через бота Telegram
            await bot.send_document(
                chat_id=query.message.chat.id,
                document=FSInputFile(path=filepath, filename=filename),
                caption='Текст для описания документа'
                )
        return

    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        text=action,
        # Передаем клавиатуру с отчетами по датам
        reply_markup=date_reports_keyboard())


@router.callback_query(DateReportsCD.filter(), IsPrivate(), IsAdmin())
async def choose_reports_period_callback(
        query: CallbackQuery, state: FSMContext) -> None:

    action = query.data.split(':')[-1]
    await query.answer(action)

    # Инициализируем подключение к базе данных
    db = Database()
    action_sender = ChatActionSender(
            bot=bot,
            chat_id=query.from_user.id,
            action=ChatAction.UPLOAD_DOCUMENT
        )
    async with action_sender:
        # Если выбран текущий месяц
        if action == DateReports.CURRENT.value:
            # Получаем текущую дату
            current_date = datetime.now().date()
            # Вычисляем текущий месяц
            begin_current_month = datetime(
                year=current_date.year,
                month=current_date.month,
                day=1).date()
            end_current_month = begin_current_month + \
                relativedelta(months=1, days=-1)
            begin = begin_current_month
            end = end_current_month
            # Выгружаем отчет и отправляем сообщение
            result = await db.select_group_events_query(begin, end)
            filepath, filename = await db.fetchdata(result, begin, end)
            await bot.send_document(
                chat_id=query.message.chat.id,
                document=FSInputFile(path=filepath, filename=filename),
                caption='Текст для описания документа'
            )
            return

        # Если выбран предыдущий месяц
        elif action == DateReports.PREVIOUS.value:
            # Получаем текущую дату
            current_date = datetime.now().date()
            # Вычисляем текущий месяц
            begin_current_month = datetime(
                year=current_date.year,
                month=current_date.month,
                day=1).date()
            end_current_month = begin_current_month + \
                relativedelta(months=1, days=-1)

            # Вычисляем предыдущий месяц
            begin_previous_month = (begin_current_month -
                                    relativedelta(months=1)
                                    ).replace(day=1)
            end_previous_month = begin_current_month - relativedelta(days=1)

            begin = begin_previous_month
            end = end_previous_month

            # Выгружаем отчет и отправляем сообщение

            result = await db.select_group_events_query(begin, end)
            filepath, filename = await db.fetchdata(result, begin, end)
            await bot.send_document(
                    chat_id=query.message.chat.id,
                    document=FSInputFile(path=filepath, filename=filename),
                    caption='Текст для описания документа'
                )
            return

    # Если выбран период
        # Назначение машинного состояния
        # await state.set_state(DatePeriod.start_message)
        # await state.update_data(start_message=query.message.message_id)
        await state.set_state(DatePeriod.period)
        await bot.edit_message_text(
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            text=add_reports_period_message(),
            # Передаем клавиатуру ввода периода
            reply_markup=back_to_reports())


@router.message(DatePeriod.period,
                IsPrivate(),
                IsAdmin()
                )
async def choose_reports_period_message(
        message: Message, state: FSMContext) -> None:
    try:
        start, end = message.text.split('-')
        # Проверка правильного формата ввода периода
        if not re.match(r'^\d{2}\.\d{2}\.\d{4}-\
                \d{2}\.\d{2}\.\d{4}$', message.text):
            await bot.delete_message(chat_id=message.chat.id,
                                     message_id=message.message_id)
            await bot.send_message(chat_id=message.chat.id,
                                   text=add_reports_period_message())
        start_date = datetime.strptime(start,
                                       '%d.%m.%Y').strftime('%Y-%m-%d')
        end_date = datetime.strptime(end,
                                     '%d.%m.%Y').strftime('%Y-%m-%d')
        begin = start_date
        end = end_date
        db = Database()
        result = await db.select_group_events_query(begin, end)
        filepath, filename = await db.fetchdata(result, begin, end)
        await bot.send_document(
            chat_id=message.chat.id,
            document=FSInputFile(path=filepath, filename=filename),
            caption='Текст для описания документа'
        )
        # Очистить машинное состояние после успешного выполнения
        await state.clear()

    except ValueError:
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id)
        await bot.send_message(chat_id=message.chat.id,
                               text=add_reports_period_message())

    return
