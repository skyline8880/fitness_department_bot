from asyncio import sleep

from aiogram import F, Router
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.bot import bot
from bot.message.admins.actions import action_message
from bot.message.admins.admin_menu import (add_admin_result_message,
                                           add_remove_admin_message,
                                           exist_admin_result_message,
                                           not_exist_admin_result_message,
                                           remove_admin_result_message,
                                           wrong_admin_phone_message)
from database.database import Database
from filters.callback_filters import (AdminMenu, AdminMenuActions,
                                      AdminMenuActionsCD, AdminsActions,
                                      AdminsActionsCD)
from filters.filters import IsAdmin, IsPhone, IsPrivate, IsText
from keyboards.admins.admins_menu import admins_keydoard, back_to_admins
from state.state import AddRemoveAdmin

router = Router()


@router.callback_query(
        AdminsActionsCD.filter(F.adm_act.in_({
            AdminsActions.ADD, AdminsActions.REMOVE})),
        IsPrivate(),
        IsAdmin())
async def admins_actions(
        query: CallbackQuery, state: FSMContext) -> None:
    action = query.data.split(':')[-1]
    await query.answer(action)
    await state.set_state(AddRemoveAdmin.action)
    await state.update_data(action=action)
    await state.update_data(start_message=query.message.message_id)
    await state.set_state(AddRemoveAdmin.phone_number)
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        text=add_remove_admin_message(action=action),
        reply_markup=back_to_admins())


@router.message(
    AddRemoveAdmin.phone_number,
    IsAdmin(),
    IsText(),
    IsPhone(),
    IsPrivate())
async def get_admins_phone(message: Message, state: FSMContext) -> None:
    db = Database()
    phone = message.text
    m_id = message.message_id + 1
    await message.delete()
    get_user = await db.select_user_by_sign(sign=phone)
    data = await state.get_data()
    action = data['action']
    if action == AdminsActions.ADD.value:
        is_allowed = True
        msg = add_admin_result_message(phone=phone)
        if get_user is not None:
            if get_user[1]:
                is_allowed = False
                msg = exist_admin_result_message(phone=phone)
        if is_allowed:
            await db.insert_into_user_admin(phone=phone, status=True)
            return await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=int(data['start_message']),
                text=msg,
                reply_markup=back_to_admins())
        await message.answer(text=msg)
        await sleep(5)
        try:
            await bot.delete_message(
                chat_id=message.from_user.id,
                message_id=m_id)
        except Exception:
            pass
        return
    is_allowed = True
    msg = remove_admin_result_message(phone=phone)
    if get_user is None:
        is_allowed = False
        msg = not_exist_admin_result_message(phone=phone)
    if get_user is not None:
        if not get_user[1]:
            is_allowed = False
            msg = not_exist_admin_result_message(phone=phone)
    if is_allowed:
        await db.update_user_is_admin_status(phone=phone, is_admin=False)
        return await bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=int(data['start_message']),
            text=msg,
            reply_markup=back_to_admins())
    await message.answer(text=msg)
    await sleep(5)
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=m_id)
    except Exception:
        pass
    return


@router.message(
    AddRemoveAdmin.phone_number,
    IsAdmin(),
    or_f(~IsText(), ~IsPhone()),
    IsPrivate())
async def get_wrong_admins_phone(message: Message, state: FSMContext) -> None:
    await message.delete()
    m_id = message.message_id + 1
    await message.answer(
        text=wrong_admin_phone_message())
    await sleep(5)
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=m_id)
    except Exception:
        pass


@router.callback_query(
        AdminMenuActionsCD.filter(F.admen_act == AdminMenuActions.ADMINS),
        IsPrivate(),
        IsAdmin())
async def to_menu_action(
        query: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        text=action_message(action=AdminMenu.ADMINS.value),
        reply_markup=admins_keydoard())