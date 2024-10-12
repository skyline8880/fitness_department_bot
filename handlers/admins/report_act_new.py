from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from filters.callback_filters import ReportsActions, ReportsActionsCD
from filters.filters import IsAdmin, IsPrivate
from filters.callback_filters import (CurrenEventActionsCD, CurrentEventActions,
                                      CustomerEventActionsCD, EventDepartment,
                                      EventPayment, EventsActions, EventsActionsCD,
                                      EventSubdivision)
import subprocess
import asyncio
import datetime
import logging

# Настройка журналирования
logging.basicConfig(filename='app_callback.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Инициализация роутера
router = Router()
"""
# Обработчик для действий с событиями пример
@router.callback_query(
        EventsActionsCD.filter(F.event_act.in_({
            EventsActions.CREATE,
            EventsActions.COMMINGEVENTS,
            EventsActions.TOSENDEVENTS})),
        IsPrivate(),
        IsAdmin())
async def events_actions(query: CallbackQuery, state: FSMContext) -> None:
    # Извлечение действия из данных коллбэка
    action = query.data.split(':')[-1
    # Извлечение действия из данных коллбэка
    await query.answer(action)
    # Отправка ответа пользователю с полученным действием
    msg = event_choose_department()
    # Создание сообщения для выбора департамента
    kbrd = await department_keydoard()
    # Получение клавиатуры с департаментами
    if action == EventsActions.COMMINGEVENTS.value:
        # Если действие - предстоящие события
        kbrd, msg = await Paginator().create_list()
        # Создание списка событий для предстоящих событий
    elif action == EventsActions.TOSENDEVENTS.value:
        # Если действие - отправить событие
        kbrd, msg = await Paginator(event_category='to_send').create_list()
        # Создание списка событий для отправки
    if kbrd is None:
        return
        # В случае отсутствия клавиатуры, завершение функции
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        text=msg,
        reply_markup=kbrd)
    # Редактирование текста сообщения с клавиатурой в чате пользователя
"""
# Обработчик для действий с отчетами
@router.callback_query(
    ReportsActionsCD.filter(F.report_act.in_({
        ReportsActions.EVENTS, ReportsActions.USERS, ReportsActions.REPORT1, ReportsActions.REPORT2 })),
    IsPrivate(),
    IsAdmin()
)
async def reports_actions(query: CallbackQuery, state: FSMContext) -> None:
    action = query.data.split(':')[-1
    await query.answer(action)
    await process_selected_date(action)

# Функция для обработки выбранной даты
async def process_selected_date(selected_date):
    logging.info(f"Выбранная дата для выгрузки файлов: {selected_date}")

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton(text="Сегодня", callback_data="today"),
        types.InlineKeyboardButton(text="Вчера", callback_data="yesterday"),
    )
    await message.answer("Выберите дату для выгрузки файлов:", reply_markup=keyboard)

# Обработчик коллбэк-запросов для выбора текущей или предыдущей даты
@dp.callback_query_handler(lambda c: c.data in ['today', 'yesterday'])
async def process_callback(callback_query: types.CallbackQuery):
    date_selected = callback_query.data

    if date_selected == 'today':
        selected_date = datetime.datetime.now().date()
    elif date_selected == 'yesterday':
        selected_date = datetime.datetime.now().date() - datetime.timedelta(days=1)

    await process_selected_date(selected_date)
