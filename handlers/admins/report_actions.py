from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from filters.callback_filters import ReportsActions, ReportsActionsCD
from filters.filters import IsAdmin, IsPrivate

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
    print(action)
