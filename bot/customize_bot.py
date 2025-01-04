from asyncio import sleep
from typing import Any, Union

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand, CallbackQuery, Message

from bot.message.admins.events import (  # customers_recievers_message,
    customer_event_data_message, customers_enroll_message, event_data_message)
from bot.message.welcome import (welcome_after_auth_choose_department_message,
                                 welcome_message)
from constants.actions import Action
from database.database import Database
from keyboards.admins.events_menu import (back_button, current_event_keyboard,
                                          customer_event_keyboard)
from keyboards.checkbox_menus import department_keydoard


class FitnessDepartmentBot(Bot):
    def __init__(
            self,
            token: str = None,
            session: None = None,
            default: None = None,
            **kwargs: Any) -> None:
        super().__init__(
            token=token,
            session=session,
            default=default,
            kwargs=kwargs)
        self.default = DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)

    async def command_init(self) -> None:
        await self.set_my_commands(
            commands=[
                BotCommand(command='start', description='Запустить бота')])

    async def clear_messages(
            self,
            message: Union[Message, CallbackQuery],
            state: FSMContext,
            finish: bool
            ) -> None:
        chat_id = message.from_user.id
        message_object = message
        if isinstance(message, CallbackQuery):
            message_object = message.message
            current_message_id = message.message.message_id
        else:
            current_message_id = message.message_id
        try:
            data = await state.get_data()
            start_message = int(data['start_message'])
            for m_id in range(current_message_id - start_message + 1):
                try:
                    await self.delete_message(
                        chat_id=chat_id,
                        message_id=current_message_id - m_id)
                except Exception:
                    pass
        except Exception:
            try:
                await message_object.delete()
            except Exception:
                pass
        if finish:
            await state.clear()

    async def add_user(
            self,
            message: Union[Message, CallbackQuery],
            state: FSMContext):
        db = Database()
        message_object = message
        if isinstance(message, CallbackQuery):
            message_object = message.message
        user_data = await state.get_data()
        user_data_from_db = await db.insert_into_user_auth(
            phone=user_data['phone_number'],
            last_name=user_data['last_name'],
            first_name=user_data['first_name'],
            patronymic=user_data['patronymic'],
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username)
        if user_data is None:
            print('Error while adding user')
            print(
                user_data['phone_number'],
                user_data['last_name'],
                user_data['first_name'],
                user_data['patronymic'],
                message.from_user.id,
                message.from_user.full_name,
                message.from_user.username)
            return
        await self.clear_messages(message=message, state=state, finish=True)
        await message_object.answer(
            text=welcome_message(first_name=user_data_from_db[4]))
        await message_object.answer(
            text=welcome_after_auth_choose_department_message(),
            reply_markup=await department_keydoard(
                telegram_id=user_data_from_db[6],
                is_admin=user_data_from_db[1],
                welcome=[Action.TOSUBDIVS]))

    async def create_event(
            self,
            query: CallbackQuery,
            state: FSMContext):
        data = await state.get_data()
        db = Database()
        add_success = await db.insert_event(data=data)
        if not add_success:
            msg = 'ОШИБКА СОЗДАНИЯ СОБЫТИЯ'
            kbrd = back_button()
        else:
            event_data = await db.select_event_by_id(event_id=add_success[0])
            msg = event_data_message(event_data=event_data)
            kbrd = current_event_keyboard(event_data=event_data)
        await self.clear_messages(message=query, state=state, finish=True)
        await query.message.answer(
            text=msg,
            reply_markup=kbrd)
        """ await self.edit_message_text(
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            text=msg,
            reply_markup=kbrd) """

    async def open_event(
            self,
            query: CallbackQuery,
            state: FSMContext,
            event_id: int):
        db = Database()
        event = await db.select_event_by_id(event_id=event_id)
        if not event:
            msg = 'ОШИБКА ОТКРЫТИЯ СОБЫТИЯ'
            kbrd = None
        else:
            msg = event_data_message(event_data=event)
            kbrd = current_event_keyboard(event_data=event)
        await self.clear_messages(message=query, state=state, finish=False)
        await query.message.answer(text=msg, reply_markup=kbrd)
        """ await self.edit_message_text(
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            text=msg,
            reply_markup=kbrd) """

    async def newsletter(
            self,
            query: CallbackQuery,
            state: FSMContext,
            event_id: int):
        db = Database()
        event = await db.select_event_by_id(event_id=event_id)
        recievers = await db.select_recievers_list(
            department_id=event[6],
            subdivision_id=event[8])
        msg = 'Нет целевой аудитории'
        kbrd = back_button()
        if recievers != []:
            for reciever in recievers:
                try:
                    await self.send_message(
                        chat_id=reciever[0],
                        text=customer_event_data_message(event),
                        reply_markup=await customer_event_keyboard(
                            event_id=event_id,
                            customer_id=reciever[0]))
                    await db.insert_reciever(
                        event_id=event_id,
                        customer_id=reciever[0])
                except Exception as e:
                    print(
                        f'Ошибка рассылки: ID события: {event_id}'
                        f' ID получателя: {reciever[0]}\n'
                        f'{e}')
            await db.update_event_sent(status=True, event_id=event_id)
            event = await db.select_event_by_id(event_id=event_id)
            msg = event_data_message(event_data=event)
            kbrd = current_event_keyboard(event_data=event)
        await self.clear_messages(message=query, state=state, finish=False)
        await query.message.answer(text=msg, reply_markup=kbrd)
        """ await self.edit_message_text(
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            text=msg,
            reply_markup=kbrd) """

    async def statistics(
            self,
            query: CallbackQuery,
            state: FSMContext,
            event_id: int):
        db = Database()
        customers_enroll = await db.select_enroll_list(event_id=event_id)
        # customers_recievers = await db.select_event_recievers_list(
        #     event_id=event_id)
        enroll_msg = customers_enroll_message(data=customers_enroll)
        # recievers_msg = customers_recievers_message(data=customers_recievers)
        await self.clear_messages(message=query, state=state, finish=False)
        await query.message.answer(text=enroll_msg, reply_markup=back_button())
        """ await self.edit_message_text(
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            text=enroll_msg,
            reply_markup=back_button()) """

    async def new_user_newsletter(self, telegram_id: int):
        db = Database()
        events_to_send = await db.select_new_user_events_to_send(
            telegram_id=telegram_id)
        counter = 0
        for event in events_to_send:
            available_to_send = await db.check_users_dep_and_subdiv(
                department_id=event[6],
                subdivision_id=event[8],
                telegram_id=telegram_id
            )
            if available_to_send is not None:
                if counter > 5:
                    await sleep(1)
                await self.send_message(
                    chat_id=telegram_id,
                    text=customer_event_data_message(event),
                    reply_markup=await customer_event_keyboard(
                        event_id=event[0],
                        customer_id=telegram_id))
                await db.insert_reciever(
                    event_id=event[0],
                    customer_id=telegram_id)
                counter += 1
