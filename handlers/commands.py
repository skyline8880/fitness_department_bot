from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.bot import bot
from bot.message.admins.admin_menu import admin_menu_message
from bot.message.auth_message import (contact_recieved_message,
                                      enter_first_name_message,
                                      enter_last_name_message,
                                      enter_patronymic_message,
                                      need_auth_message, wrong_contact_message,
                                      wrong_text_message_message)
from bot.message.user_menu import user_menu_message
from database.database import Database
from filters.callback_filters import Action, ActionsCD
from filters.filters import (IsAdmin, IsAuth, IsDev, IsPrivate,
                             MessageIsValidContact)
from filters.name_validator import fullname_validator
from keyboards.admins.main_menu import admin_keydoard
from keyboards.auth import (cancel_and_skip_keyboard, cancel_keyboard,
                            get_contact_keyboard, remove_conact_keyboard)
from keyboards.menu_keyboard import menu_keyboard
from state.state import AuthStart

router = Router()


@router.message(Command('dev'), IsDev(), IsPrivate())
async def dev_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    db = Database()
    await db.insert_into_user_auth(
        phone='79998533965',
        last_name='Холов',
        first_name='Сайфуллои',
        patronymic='Абдурахмон',
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username)
    await db.update_user_is_admin_status(
        is_admin=True, phone='79998533965')


@router.message(Command('del'), IsDev(), IsAuth(), IsPrivate())
async def del_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    db = Database()
    await db.update_user_is_admin_status(
        is_admin=False, phone='79998533965')


@router.message(Command('start'), ~IsAuth(), IsPrivate())
async def start_unauth_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(AuthStart.start_message)
    await state.update_data(start_message=message.message_id + 1)
    await state.set_state(AuthStart.phone_number)
    await message.answer(
        text=need_auth_message(message.from_user.full_name),
        reply_markup=get_contact_keyboard)


@router.message(Command('start'), IsAuth(), ~IsAdmin(), IsPrivate())
async def start_user_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    db = Database()
    user_data = await db.select_user_by_sign(sign=message.from_user.id)
    await message.answer(
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
                    telegram_id=message.from_user.id)
                if status is not None
            ],
            subdivs=[
                subdiv
                for
                _,
                subdiv,
                status
                in await db.select_user_references_by_sign(
                    telegram_id=message.from_user.id)
                if status is not None
            ]
        ),
        reply_markup=menu_keyboard())


@router.message(Command('start'), IsAuth(), IsAdmin(), IsPrivate())
async def start_admin_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    db = Database()
    user_data = await db.select_user_by_sign(sign=message.from_user.id)
    await message.answer(
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
                    telegram_id=message.from_user.id)
                if status is not None
            ],
            subdivs=[
                subdiv
                for
                _,
                subdiv,
                status
                in await db.select_user_references_by_sign(
                    telegram_id=message.from_user.id)
                if status is not None
            ]
        ),
        reply_markup=menu_keyboard())
    await message.answer(
        text=admin_menu_message(
            first_name=user_data[4],
            phone=user_data[2]),
        reply_markup=admin_keydoard())


@router.message(AuthStart.phone_number, MessageIsValidContact(), IsPrivate())
async def get_contact(message: Message, state: FSMContext) -> None:
    phone_number = message.contact.phone_number.replace('+', '')
    await state.update_data(phone_number=phone_number)
    await state.set_state(AuthStart.last_name)
    await bot.clear_messages(
        message=message, state=state, finish=False)
    await message.answer(
        text=contact_recieved_message(),
        reply_markup=remove_conact_keyboard)
    await message.answer(
        text=enter_last_name_message(),
        reply_markup=cancel_keyboard())


@router.message(AuthStart.phone_number, ~MessageIsValidContact(), IsPrivate())
async def get_wrong_contact(message: Message, state: FSMContext) -> None:
    await message.delete()
    await message.answer(
        text=wrong_contact_message(),
        reply_markup=get_contact_keyboard)


@router.message(AuthStart.last_name, IsPrivate())
async def get_last_name(message: Message, state: FSMContext) -> None:
    valid_input = fullname_validator(message=message)
    if not valid_input:
        await message.delete()
        await message.answer(
            text=wrong_text_message_message())
        return
    await bot.clear_messages(
        message=message, state=state, finish=False)
    await state.update_data(last_name=valid_input)
    await state.set_state(AuthStart.first_name)
    await message.answer(
        text=enter_first_name_message(),
        reply_markup=cancel_keyboard())


@router.message(AuthStart.first_name, IsPrivate())
async def get_first_name(message: Message, state: FSMContext) -> None:
    valid_input = fullname_validator(message=message)
    if not valid_input:
        await message.delete()
        await message.answer(
            text=wrong_text_message_message())
        return
    await bot.clear_messages(
        message=message, state=state, finish=False)
    await state.update_data(first_name=valid_input)
    await state.set_state(AuthStart.patronymic)
    await message.answer(
        text=enter_patronymic_message(),
        reply_markup=cancel_and_skip_keyboard())


@router.message(AuthStart.patronymic, IsPrivate())
async def get_patronymic(message: Message, state: FSMContext) -> None:
    valid_input = fullname_validator(message=message)
    if not valid_input:
        await message.delete()
        await message.answer(
            text=wrong_text_message_message())
        return
    await state.update_data(patronymic=valid_input)
    await bot.add_user(message=message, state=state)


@router.callback_query(
        ActionsCD.filter(F.action.in_({Action.SKIP, Action.CANCEL})),
        IsPrivate())
async def cancel_and_skip_action(
        query: CallbackQuery, state: FSMContext) -> None:
    action = query.data.split(':')[-1]
    if action == Action.SKIP.value:
        await state.update_data(patronymic=None)
        await bot.add_user(message=query, state=state)
        return
    await bot.clear_messages(
        message=query, state=state, finish=True)
