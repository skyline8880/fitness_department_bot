from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.bot import bot
from bot.message.admins.actions import action_message
from bot.message.admins.admin_menu import admin_menu_message
from database.database import Database
from filters.callback_filters import (AdminMenu, AdminMenuActions,
                                      AdminMenuActionsCD, AdminMenuCD)
from filters.filters import IsAdmin, IsPrivate
from keyboards.admins.admins_menu import admins_keydoard
from keyboards.admins.events_menu import events_keydoard
from keyboards.admins.main_menu import admin_keydoard
from keyboards.admins.reports_menu import reports_keydoard

router = Router()


@router.callback_query(
        AdminMenuCD.filter(F.adm_menu.in_({
            AdminMenu.ADMINS, AdminMenu.EVENTS, AdminMenu.REPORTS})),
        IsPrivate(),
        IsAdmin())
async def admin_menu_actions(
        query: CallbackQuery, state: FSMContext) -> None:
    action = query.data.split(':')[-1]
    await query.answer(action)
    kbrd = admins_keydoard
    if action == AdminMenu.EVENTS.value:
        kbrd = events_keydoard
    elif action == AdminMenu.REPORTS.value:
        kbrd = reports_keydoard
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        text=action_message(action=action),
        reply_markup=kbrd())


@router.callback_query(
        AdminMenuActionsCD.filter(F.admen_act == AdminMenuActions.TOMENU),
        IsPrivate(),
        IsAdmin())
async def to_menu_action(
        query: CallbackQuery, state: FSMContext) -> None:
    action = query.data.split(':')[-1]
    await query.answer(action)
    await state.clear()
    db = Database()
    user_data = await db.select_user_by_sign(sign=query.from_user.id)
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        text=admin_menu_message(
            first_name=user_data[4],
            phone=user_data[2]),
        reply_markup=admin_keydoard())


@router.callback_query(
        AdminMenuActionsCD.filter(F.admen_act == AdminMenuActions.BACK),
        IsPrivate(),
        IsAdmin())
async def back_action(
        query: CallbackQuery, state: FSMContext) -> None:
    action = query.data.split(':')[-1]
    await query.answer(action)
    await state.clear()
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        text=action_message(action=action),
        reply_markup=events_keydoard())