from aiogram import F, Router
from aiogram.types import InputFile, CallbackQuery
from aiogram.enums.chat_action import ChatAction, ChatActionSender
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from filters.callback_filters import ReportsActions, ReportsActionsCD
from filters.filters import IsAdmin, IsPrivate
from database.database import Database
from keyboards import event_reports_handler 
import datetime
import logging
from keyboards.admins.date_menu import range_options
from bot.bot import bot

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = Router()

@router.callback_query(
    ReportsActionsCD.filter(F.report_act.in_({
        ReportsActions.EVENTS, ReportsActions.USERS})),
    IsPrivate(),
    IsAdmin()
)
async def reports_actions(query: CallbackQuery, state: FSMContext) -> None:
    action = query.data.split(':')[-1]
    await query.answer(action)
    db = Database()
   
    if action == ReportsActions.USERS.value:
        chat_action = ChatAction.UPLOAD_DOCUMEN
        action_sender = ChatActionSender(
            bot=bot,
            chat_id=query.from_user.id,
            action=ChatAction.UPLOAD_DOCUMENT
        )
        async with db.connect():
            result = await db.select_subscribers_query()
            filename = await db.subscribers(result)
            report_path = f'reports/{filename}'
            await bot.send_document(
                chat_id=query.message.chat.id,
                document=InputFile(path=report_path, filename=filename)
            )
            
        return

 
@router.callback_query(
    ReportsActionsCD.filter(F.report_act.in_({
        ReportsActions.EVENTS})),
    IsPrivate(),
    IsAdmin()
)
async def events_reports_handler(query: CallbackQuery, state: FSMContext) -> None:
    keyboard = InlineKeyboardMarkup()

 # Функция для обработки нажатий на кнопки клавиатуры
async def handle_button_click(call: CallbackQuery):
    data = call.data
    
    # Проверяем, какая кнопка была нажата
    if data == "event_date_report:current_month":
        await call.answer("Processing current month selection")  # Выполнение функции для текущего месяца
    
    elif data == "event_date_report:previous_month":
        await call.answer("Processing previous month selection")  # Выполнение функции для предыдущего месяца
    
    elif data == "event_date_report:date_range":
        await call.answer("Processing date range selection")  # Выполнение функции для диапазона дат
    
    elif data == "to_menu":
        await call.answer("Going back to main menu")  # Выполнение функции для возврата в главное меню

 if r_type == 'month':
                add = self.date + relativedelta(months=1)
                take = self.date - relativedelta(months=1)
    return 


"""# Роут для обработки нажатий на кнопки клавиатуры
@router.callback_query()
async def handle_keyboard_buttons(call: CallbackQuery = Depends(handle_button_click)):
    await call.answer()

# Роут для отправки клавиатуры
@router.get("/send_keyboard")
async def send_keyboard():
    keyboard = events_reports_keyboard()  # Создаем клавиатуру с кнопками
    # Отправляем клавиатуру пользователю (метод отправки зависит от используемого мессенджера или бот-фреймворка)
    return {"message": "Choose an option", "keyboard": keyboard}"""
   