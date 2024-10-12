import subprocess

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from filters.callback_filters import ReportsActions, ReportsActionsCD
from filters.filters import IsAdmin, IsPrivate
from aiogram.types import Message
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = Router()

# Добавляем обработку subprocess.run
async def run_script(script_name: str):
    try:
        result = subprocess.run(["python", script_name], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        logging.info(f"Ошибка выполнения скрипта {script_name}: {e}")

@router.callback_query(
    ReportsActionsCD.filter(
        F.report_act.in_({
            ReportsActions.EVENTS, ReportsActions.USERS, ReportsActions.REPORT1, ReportsActions.REPORT2 })),
    IsPrivate(),
    IsAdmin())
async def reports_actions(query: CallbackQuery, state: FSMContext) -> None:
    action = query.data.split(':')[-1]
    
    if action == ReportsActions.REPORT1:
        await run_script("rep1.py")  # Отчет1
        logging.info(f"Скрипт для {ReportsActions.REPORT1} выполнен")
    elif action == ReportsActions.REPORT2:
        await run_script("rep2.py")  # Отчет2
        logging.info(f"Скрипт для {ReportsActions.REPORT2} выполнен")
    else:
        await query.answer(action)

    print(action)