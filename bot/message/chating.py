from aiogram.enums.chat_type import ChatType
from aiogram.types import Message
from aiogram.utils import markdown


def message_placeholder(
        message: Message,
        users_data,
        text,
        message_id,
        chat_id,
        event_data=None):
    (
        user_id,
        is_admin,
        phone,
        last_name,
        first_name,
        patronymic,
        telegram_id,
        fullname,
        username,
        department_id,
        subdiv_references
    ) = users_data
    print(event_data)
    code_info = markdown.text(
        markdown.markdown_decoration.quote('код:'),
        markdown.markdown_decoration.code(f'{message_id}/{chat_id}'))
    if message.chat.type == ChatType.PRIVATE:
        sender_obj = markdown.text(
            markdown.text(
                markdown.markdown_decoration.quote('пользователь:'),
                markdown.markdown_decoration.quote(
                    f'{last_name} {first_name}')),
            markdown.text(
                markdown.markdown_decoration.quote('телефон:'),
                markdown.markdown_decoration.code(phone)),
            sep='\n')
        if event_data:
            (
                event_id,
                event_date,
                _,
                creator_lname,
                creator_fname,
                creator_phone,
                _,
                department,
                _,
                subdivision,
                event_name,
                event_description,
                event_isfree,
                event_isactive,
                event_sent,
                _,
                executor
            ) = event_data
            event_obj = markdown.text(
                markdown.text(
                    markdown.markdown_decoration.quote('событие:'),
                    markdown.markdown_decoration.quote(event_name)),
                markdown.text(
                    markdown.markdown_decoration.quote('дата:'),
                    markdown.markdown_decoration.quote(
                        f'{event_date:%d.%m.%Y в %H:%M}')),
                markdown.text(
                    markdown.markdown_decoration.quote('в клубе:'),
                    markdown.markdown_decoration.quote(department)),
                markdown.text(
                    markdown.markdown_decoration.quote('подразделении:'),
                    markdown.markdown_decoration.quote(subdivision)),
                sep='\n')
            sender_obj += f'\n{event_obj}'
        code_info += f'\n{sender_obj}'
    basic_info = markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote('сообщение:'),
            markdown.markdown_decoration.quote(text)),
        sep='\n')
    return f'{code_info}\n{basic_info}'


def chating_hint() -> str:
    return markdown.text(
        markdown.markdown_decoration.quote(
            'Если хотите задать вопрос,\n'
            'то выберите сообщение бота,\n'
            'содержащее ключевое слово "код" или\n'
            'информацию о мероприятии, затем\n'
            'выберите действие "Ответить" и\n'
            'Ваше сообщение будет направлено\n'
            'сотрудникам.\n'))
