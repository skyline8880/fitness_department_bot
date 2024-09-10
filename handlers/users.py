from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.bot import bot
from bot.message.user_menu import (user_choose_depart_message,
                                   user_choose_subdiv_message,
                                   user_menu_message)
from bot.message.welcome import welcome_after_auth_choose_subdivision_message
from database.database import Database
from filters.callback_filters import (Action, ActionsCD, DepartmentsCD, Menu,
                                      MenuCD, ReferencesCD)
from filters.filters import IsAdmin, IsAuth, IsPrivate
from keyboards.checkbox_menus import department_keydoard, subdivision_keydoard
from keyboards.menu_keyboard import menu_keyboard

router = Router()


@router.callback_query(
        ActionsCD.filter(F.action == Action.TOSUBDIVS),
        IsPrivate(),
        IsAuth(),
        ~IsAdmin())
async def to_subdivs_after_auth(query: CallbackQuery) -> None:
    action = query.data.split(':')[-1]
    await query.answer(action)
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        text=welcome_after_auth_choose_subdivision_message(),
        reply_markup=await subdivision_keydoard(
            telegram_id=query.from_user.id, welcome=[Action.TOMENU]))


@router.callback_query(
        ActionsCD.filter(F.action == Action.TOMENU),
        IsPrivate(),
        IsAuth(),
        ~IsAdmin())
async def to_menu_action(query: CallbackQuery) -> None:
    action = query.data.split(':')[-1]
    await query.answer(action)
    db = Database()
    user_data = await db.select_user_by_sign(sign=query.from_user.id)
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        text=user_menu_message(
            last_name=user_data[3],
            first_name=user_data[4],
            clubs=[
                club
                for
                _,
                club,
                status
                in await db.select_user_departments_by_sign(
                    telegram_id=query.from_user.id)
                if status is not None
            ],
            subdivs=[
                subdiv
                for
                _,
                subdiv,
                status
                in await db.select_user_references_by_sign(
                    telegram_id=query.from_user.id)
                if status is not None
            ]
        ),
        reply_markup=menu_keyboard())


@router.callback_query(
        MenuCD.filter(F.menu_act.in_({Menu.CLUB, Menu.SUBDIV})),
        IsPrivate(),
        IsAuth(),
        ~IsAdmin())
async def menu_buttons_choose(query: CallbackQuery) -> None:
    action = query.data.split(':')[-1]
    await query.answer(action)
    method = department_keydoard
    msg = user_choose_depart_message()
    if action == Menu.SUBDIV.value:
        method = subdivision_keydoard
        msg = user_choose_subdiv_message()
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        text=msg,
        reply_markup=await method(
            telegram_id=query.from_user.id, welcome=[Action.TOMENU]))


@router.callback_query(
        DepartmentsCD.filter(),
        IsPrivate(),
        IsAuth(),
        ~IsAdmin())
async def choose_department(query: CallbackQuery) -> None:
    db = Database()
    dep_id, status = query.data.split(':')[1:]
    is_add = False
    msg = 'Исключён клуб'
    if int(status) == 0:
        is_add = True
        msg = 'Добавлен клуб'
    await query.answer(msg)
    await db.update_add_remove_users_department(
        depatment_id=int(dep_id),
        telegram_id=query.from_user.id,
        is_add=is_add)
    additional_button = [Action.TOMENU]
    if 'Добро пожаловать' in query.message.text:
        additional_button = [Action.TOSUBDIVS]
    await query.message.edit_reply_markup(
        reply_markup=await department_keydoard(
            query.from_user.id,
            welcome=additional_button))


@router.callback_query(
        ReferencesCD.filter(),
        IsPrivate(),
        IsAuth(),
        ~IsAdmin())
async def choose_subdivision(query: CallbackQuery) -> None:
    db = Database()
    subdiv_id, status = query.data.split(':')[1:]
    is_add = False
    msg = 'Исключено подразделение'
    if int(status) == 0:
        is_add = True
        msg = 'Добавлено подразделение'
    await query.answer(msg)
    await db.update_add_remove_users_subdivision(
        subdivision_id=int(subdiv_id),
        telegram_id=query.from_user.id,
        is_add=is_add)
    await query.message.edit_reply_markup(
        reply_markup=await subdivision_keydoard(
            query.from_user.id,
            welcome=[Action.TOMENU]))
