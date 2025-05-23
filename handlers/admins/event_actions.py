import datetime as dt
from asyncio import sleep

from aiogram import F, Router
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bitrix_api.requests import send_bitrix_request
from bot.bot import bot
from bot.message.admins.events import (event_add_photo, event_choose_date,
                                       event_choose_department,
                                       event_choose_description,
                                       event_choose_executor,
                                       event_choose_hour, event_choose_is_free,
                                       event_choose_minute, event_choose_name,
                                       event_choose_r_type,
                                       event_choose_subdivision,
                                       events_choose_page, wrong_executor,
                                       wrong_executor_length,
                                       wrong_photo_format, wrong_text_format,
                                       wrong_text_length)
from database.database import Database
from filters.callback_filters import (CurrenEventActionsCD,
                                      CurrentEventActions,
                                      CustomerEventActionsCD, EventDepartment,
                                      EventPayment, EventsActions,
                                      EventsActionsCD, EventSubdivision,
                                      SkipPhoto, SkipPhotoCD)
from filters.filters import IsAdmin, IsAuth, IsPhoto, IsPrivate, IsText
from keyboards.admins.date_menu import (DateMove, DatePick, DatePicker,
                                        DateRange, OpenRange, ScrollRange)
from keyboards.admins.departs_and_subdivs import (department_keydoard,
                                                  subdivision_keydoard)
from keyboards.admins.event_pagination import (CurrentPageRangeCD,
                                               EventPageRangeCD,
                                               GetCurrentEventCD, NavigationCD,
                                               Paginator)
from keyboards.admins.events_menu import (back_button, customer_event_keyboard,
                                          free_type_keyboard)
from keyboards.admins.time_menu import (HourPicker, MinutePicker, TimeHour,
                                        TimeMinute)
from state.state import AddEventAdmin

router = Router()


@router.callback_query(
        EventsActionsCD.filter(F.event_act.in_({
            EventsActions.CREATE,
            EventsActions.COMMINGEVENTS,
            EventsActions.TOSENDEVENTS})),
        IsPrivate(),
        IsAdmin())
async def events_actions(
        query: CallbackQuery, state: FSMContext) -> None:
    action = query.data.split(':')[-1]
    await query.answer(action)
    msg = event_choose_department()
    kbrd = await department_keydoard()
    if action == EventsActions.COMMINGEVENTS.value:
        kbrd, msg = await Paginator().create_list()
    elif action == EventsActions.TOSENDEVENTS.value:
        kbrd, msg = await Paginator(event_category='to_send').create_list()
    if kbrd is None:
        return
    await bot.clear_messages(message=query, state=state, finish=False)
    await query.message.answer(text=msg, reply_markup=kbrd)


@router.callback_query(
        NavigationCD.filter(),
        IsPrivate(),
        IsAdmin())
async def event_list_navigation(
        query: CallbackQuery, state: FSMContext) -> None:
    event_category, page = query.data.split(':')[1:]
    await query.answer(f'{page}')
    kbrd, msg = await Paginator(
        event_category=event_category,
        page=int(page)).create_list()
    if kbrd is None:
        return
    await bot.clear_messages(message=query, state=state, finish=False)
    await query.message.answer(text=msg, reply_markup=kbrd)


@router.callback_query(
        EventPageRangeCD.filter(),
        IsPrivate(),
        IsAdmin())
async def event_page_range(
        query: CallbackQuery, state: FSMContext) -> None:
    event_category, page, max_pages = query.data.split(':')[1:]
    await query.answer(f'{page}')
    kbrd = await Paginator(
        event_category=event_category,
        max_pages=int(max_pages)).page_range()
    if kbrd is None:
        return
    await bot.clear_messages(message=query, state=state, finish=False)
    await query.message.answer(text=events_choose_page(), reply_markup=kbrd)


@router.callback_query(
        CurrentPageRangeCD.filter(),
        IsPrivate(),
        IsAdmin())
async def current_page_choose(
        query: CallbackQuery, state: FSMContext) -> None:
    event_category, page = query.data.split(':')[1:]
    await query.answer(f'{page}')
    kbrd, msg = await Paginator(
        event_category=event_category,
        page=int(page)).create_list()
    if kbrd is None:
        return
    await bot.clear_messages(message=query, state=state, finish=False)
    await query.message.answer(text=msg, reply_markup=kbrd)


@router.callback_query(
        GetCurrentEventCD.filter(),
        IsPrivate(),
        IsAdmin())
async def current_event_choose(
        query: CallbackQuery, state: FSMContext) -> None:
    event_id = query.data.split(':')[-1]
    await query.answer(f'{event_id}')
    await bot.open_event(
        query=query,
        state=state,
        event_id=int(event_id))


@router.callback_query(
        CurrenEventActionsCD.filter(),
        IsPrivate(),
        IsAdmin())
async def current_event_actions(
        query: CallbackQuery, state: FSMContext) -> None:
    action, event_id = query.data.split(':')[1:]
    await query.answer(f'{action}')
    db = Database()
    if action == CurrentEventActions.SEND.value:
        await bot.newsletter(query=query, state=state, event_id=event_id)
    elif action == CurrentEventActions.STATS.value:
        await bot.statistics(query=query, state=state, event_id=event_id)
    else:
        STATUS = {
            CurrentEventActions.ACTIVATE.value: True,
            CurrentEventActions.DELETE.value: False}
        await db.update_event_status(status=STATUS[action], event_id=event_id)
        await bot.open_event(
            query=query,
            state=state,
            event_id=int(event_id))


@router.callback_query(
        EventDepartment.filter(),
        IsPrivate(),
        IsAdmin())
async def event_department_choose(
        query: CallbackQuery, state: FSMContext) -> None:
    depart_id = int(query.data.split(':')[-1])
    await query.answer(f'Код клуба: {depart_id}')
    await state.set_state(AddEventAdmin.start_message)
    await state.update_data(start_message=query.message.message_id)
    await state.set_state(AddEventAdmin.creator)
    await state.update_data(creator=query.from_user.id)
    await state.set_state(AddEventAdmin.department_id)
    await state.update_data(department_id=depart_id)
    await state.set_state(AddEventAdmin.subdivision_id)
    await bot.clear_messages(message=query, state=state, finish=False)
    await query.message.answer(
        text=event_choose_subdivision(),
        reply_markup=await subdivision_keydoard())


@router.callback_query(
        EventSubdivision.filter(),
        IsPrivate(),
        IsAdmin())
async def event_subdivision_choose(
        query: CallbackQuery, state: FSMContext) -> None:
    subdiv_id = int(query.data.split(':')[-1])
    await query.answer(f'Код подразделения: {subdiv_id}')
    await state.update_data(subdivision_id=subdiv_id)
    await state.set_state(AddEventAdmin.event_date)
    await bot.clear_messages(message=query, state=state, finish=False)
    await query.message.answer(
        text=event_choose_date(),
        reply_markup=DatePicker())


@router.callback_query(
        DateMove.filter(),
        IsPrivate(),
        IsAdmin())
async def event_date_move_actions(
        query: CallbackQuery, state: FSMContext) -> None:
    year, month, day = query.data.split(':')[1:]
    await query.answer(f'{int(day):02d}.{int(month):02d}.{int(year)}')
    await bot.clear_messages(message=query, state=state, finish=False)
    await query.message.answer(
        text=event_choose_date(),
        reply_markup=DatePicker(
            year=int(year),
            month=int(month),
            day=int(day)))


@router.callback_query(
        ScrollRange.filter(),
        IsPrivate(),
        IsAdmin())
async def event_scroll_year_actions(
        query: CallbackQuery, state: FSMContext) -> None:
    year, month, day, r_type = query.data.split(':')[1:]
    await query.answer(f'{int(day):02d}.{int(month):02d}.{int(year)}')
    await bot.clear_messages(message=query, state=state, finish=False)
    await query.message.answer(
        text=event_choose_r_type(r_type=r_type),
        reply_markup=DateRange(
            r_type=r_type,
            year=int(year),
            month=int(month),
            day=int(day)))


@router.callback_query(
        OpenRange.filter(),
        IsPrivate(),
        IsAdmin())
async def event_open_range_actions(
        query: CallbackQuery, state: FSMContext) -> None:
    year, month, day, r_type = query.data.split(':')[1:]
    await query.answer(f'{int(day):02d}.{int(month):02d}.{int(year)}')
    await bot.clear_messages(message=query, state=state, finish=False)
    await query.message.answer(
        text=event_choose_r_type(r_type=r_type),
        reply_markup=DateRange(
            r_type=r_type,
            year=int(year),
            month=int(month),
            day=int(day)))


@router.callback_query(
        DatePick.filter(),
        IsPrivate(),
        IsAdmin())
async def event_datepick_actions(
        query: CallbackQuery, state: FSMContext) -> None:
    year, month, day = query.data.split(':')[1:]
    if day == '0':
        return await query.answer("Выберите день")
    date = dt.datetime(
        year=int(year),
        month=int(month),
        day=int(day))
    if date < dt.datetime.now():
        return await query.answer(
            f'Недопустимое значение: {date:%d.%m.%Y}!')
    await query.answer(f'{date:%d.%m.%Y}')
    await bot.clear_messages(message=query, state=state, finish=False)
    await query.message.answer(
        text=event_choose_hour(),
        reply_markup=HourPicker(
            year=int(year),
            month=int(month),
            day=int(day)))


@router.callback_query(
        TimeHour.filter(),
        IsPrivate(),
        IsAdmin())
async def event_timehour_actions(
        query: CallbackQuery, state: FSMContext) -> None:
    year, month, day, hour = query.data.split(':')[1:]
    await query.answer(f'{int(hour):02d}')
    await bot.clear_messages(message=query, state=state, finish=False)
    await query.message.answer(
        text=event_choose_minute(),
        reply_markup=MinutePicker(
            year=int(year),
            month=int(month),
            day=int(day),
            hour=int(hour)))


@router.callback_query(
        TimeMinute.filter(),
        IsPrivate(),
        IsAdmin())
async def event_timeminute_actions(
        query: CallbackQuery, state: FSMContext) -> None:
    year, month, day, hour, minute = query.data.split(':')[1:]
    date = dt.datetime(
        year=int(year),
        month=int(month),
        day=int(day),
        hour=int(hour),
        minute=int(minute),
        second=0)
    if date < dt.datetime.now():
        return await query.answer(
            f'Недопустимое значение: {date:%d.%m.%Y %H:%M}!')
    await state.update_data(event_date=date)
    # await state.update_data(start_message=query.message.message_id)
    await state.set_state(AddEventAdmin.photo)
    await bot.clear_messages(message=query, state=state, finish=False)
    await query.message.answer(
        text=event_add_photo(),
        reply_markup=back_button(expecting_photo=True))


@router.message(AddEventAdmin.photo, IsPhoto(), IsAdmin(), IsPrivate())
async def get_event_photo(message: Message, state: FSMContext) -> None:
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(AddEventAdmin.name)
    await bot.clear_messages(message=message, state=state, finish=False)
    await message.answer(
        text=event_choose_name(),
        reply_markup=back_button())


@router.message(AddEventAdmin.photo, ~IsPhoto(), IsAdmin(), IsPrivate())
async def get_wrong_event_photo(message: Message) -> None:
    m_id = message.message_id + 1
    try:
        await message.delete()
    except Exception as e:
        print(f'wrong message delete error {e}')
    await message.answer(text=wrong_photo_format())
    await sleep(5)
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=m_id)
    except Exception as e:
        print(f'message was deleted by user {e}')


@router.callback_query(
        SkipPhotoCD.filter(
            F.skip_photo == SkipPhoto.NOPHOTO),
        IsPrivate(),
        IsAdmin())
async def skip_event_photo(
        query: CallbackQuery, state: FSMContext) -> None:
    action = query.data.split(':')[-1]
    await query.answer(action)
    await state.update_data(photo=None)
    await state.set_state(AddEventAdmin.name)
    await bot.clear_messages(message=query, state=state, finish=False)
    await query.message.answer(
        text=event_choose_name(),
        reply_markup=back_button())


@router.message(AddEventAdmin.name, IsText(), IsAdmin(), IsPrivate())
async def get_event_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    # data = await state.get_data()
    await state.set_state(AddEventAdmin.description)
    await bot.clear_messages(message=message, state=state, finish=False)
    await message.answer(
        text=event_choose_description(),
        reply_markup=back_button())


@router.message(AddEventAdmin.description, IsText(), IsAdmin(), IsPrivate())
async def get_event_description(message: Message, state: FSMContext) -> None:
    if len(message.text) > 814:
        await message.reply(
            text=wrong_text_length(
                current_length=len(message.text),
                available_length=814
            )
        )
        return
    await state.update_data(description=message.text)
    # data = await state.get_data()
    await state.set_state(AddEventAdmin.executor)
    await bot.clear_messages(message=message, state=state, finish=False)
    await message.answer(
        text=event_choose_executor(),
        reply_markup=back_button())


@router.message(AddEventAdmin.executor, IsText(), IsAdmin(), IsPrivate())
async def get_event_executor(message: Message, state: FSMContext) -> None:
    executor = None
    try:
        lname, fname = message.text.split()
        executor = f"{lname.capitalize()} {fname.capitalize()}"
    except Exception:
        return await message.reply(
                    text=wrong_executor())
    if len(executor) > 100:
        return await message.reply(
            text=wrong_executor_length(
                current_length=len(executor)))
    await state.update_data(executor=executor)
    # data = await state.get_data()
    await state.set_state(AddEventAdmin.isfree)
    await bot.clear_messages(message=message, state=state, finish=False)
    await message.answer(
        text=event_choose_is_free(),
        reply_markup=free_type_keyboard())


@router.message(AddEventAdmin.executor, ~IsText(), IsAdmin(), IsPrivate())
async def get_wrong_event_executor(
        message: Message, state: FSMContext) -> None:
    m_id = message.message_id + 1
    try:
        await message.delete()
    except Exception as e:
        print(f'wrong message delete error {e}')
    await message.answer(text=wrong_executor())
    await sleep(5)
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=m_id)
    except Exception as e:
        print(f'message was deleted by user {e}')


@router.message(
        or_f(AddEventAdmin.name, AddEventAdmin.description),
        ~IsText(), IsAdmin(), IsPrivate())
async def get_wrong_name_or_description(
        message: Message, state: FSMContext) -> None:
    m_id = message.message_id + 1
    try:
        await message.delete()
    except Exception as e:
        print(f'wrong message delete error {e}')
    await message.answer(text=wrong_text_format())
    await sleep(5)
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=m_id)
    except Exception as e:
        print(f'message was deleted by user {e}')


@router.callback_query(
        EventPayment.filter(),
        IsPrivate(),
        IsAdmin())
async def event_payment_actions(
        query: CallbackQuery, state: FSMContext) -> None:
    code, name = query.data.split(':')[1:]
    await query.answer(name)
    await state.update_data(isfree=int(code))
    await bot.create_event(query=query, state=state)


@router.callback_query(
        CustomerEventActionsCD.filter(),
        IsPrivate(),
        IsAuth())
async def customer_event_actions(
        query: CallbackQuery, state: FSMContext) -> None:
    act_id, act_name, event_id = query.data.split(':')[1:]
    await query.answer(act_name)
    db = Database()
    await db.insert_enroll(
        event_id=event_id,
        customer_id=query.from_user.id,
        enrollaction_id=act_id)
    try:
        await bot.edit_message_reply_markup(
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            reply_markup=await customer_event_keyboard(
                event_id=event_id,
                customer_id=query.from_user.id))
        await send_bitrix_request(
            telegram_id=query.from_user.id,
            event_id=event_id,
            act_id=act_id,
            act_name=act_name)
    except Exception as e:
        print(
            f'Пользователь - query.from_user.id: {query.from_user.id} '
            f'повторно выбрал активность - act_name: {act_name}\n'
            f'Описание: {e}'
        )
