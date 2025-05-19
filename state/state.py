from aiogram.fsm.state import State, StatesGroup


class AuthStart(StatesGroup):
    start_message = State()
    phone_number = State()
    last_name = State()
    first_name = State()
    patronymic = State()


class AddRemoveAdmin(StatesGroup):
    start_message = State()
    action = State()
    phone_number = State()


class AddEventAdmin(StatesGroup):
    start_message = State()
    creator = State()
    department_id = State()
    subdivision_id = State()
    event_date = State()
    photo = State()
    name = State()
    description = State()
    executor = State()
    isfree = State()


class DatePeriod(StatesGroup):
    start_message = State()
    action = State()
    period = State()
