import datetime as dt

from aiogram.utils import markdown


def event_choose_department():
    return markdown.text(
        markdown.markdown_decoration.quote(
                'Выберите клуб, в котором'),
        markdown.markdown_decoration.quote(
                'будет проходить событие.'),
        sep='\n')


def event_choose_subdivision():
    return markdown.text(
        markdown.markdown_decoration.quote(
                'Теперь, выберите подразделение'),
        sep='\n')


def event_choose_date():
    return markdown.text(
        markdown.markdown_decoration.quote(
                'Выберите дату проведения события.'),
        sep='\n')


def event_choose_hour():
    return markdown.text(
        markdown.markdown_decoration.quote(
                'Установите час начала события.'),
        sep='\n')


def event_choose_minute():
    return markdown.text(
        markdown.markdown_decoration.quote(
                'Установите минуты начала события.'),
        sep='\n')


def event_choose_r_type(r_type):
    choice = 'год'
    if r_type == 'month':
        choice = 'месяц'
    return markdown.text(
        markdown.markdown_decoration.quote(
                f'Выберите {choice} из списка.'),
        sep='\n')


def event_add_photo():
    return markdown.text(
        markdown.markdown_decoration.quote(
                'Добавьте изображение события.'),
        sep='\n')


def event_choose_name():
    return markdown.text(
        markdown.markdown_decoration.quote(
                'Введите название события.'),
        sep='\n')


def event_choose_description():
    return markdown.text(
        markdown.markdown_decoration.quote(
                'Дайте краткое описание событию.'),
        sep='\n')


def event_choose_is_free():
    return markdown.text(
        markdown.markdown_decoration.quote(
                'Участие будет платным?'),
        sep='\n')


def comming_events_list():
    return markdown.text(
        markdown.markdown_decoration.quote(
                'Список предстоящих событий.'),
        sep='\n')


def events_to_send_list():
    return markdown.text(
        markdown.markdown_decoration.quote(
                'Список событий к рассылке.'),
        sep='\n')


def events_choose_page():
    return markdown.text(
        markdown.markdown_decoration.quote(
                'Выберите страницу.'),
        sep='\n')


def wrong_text_format():
    return markdown.text(
        markdown.markdown_decoration.quote(
                'Некорректный формат ввода!'),
        markdown.markdown_decoration.quote(
                'Введите текстовое сообщение.'),
        sep='\n')


def wrong_text_length(current_length, available_length):
    return markdown.text(
        markdown.markdown_decoration.quote(
                'Слишком длинное описание'),
        markdown.markdown_decoration.quote(
                f'Доступно не более {available_length} симовлов'),
        markdown.markdown_decoration.quote(
                f'Вы внесли {current_length}'),
        sep='\n')


def wrong_photo_format():
    return markdown.text(
        markdown.markdown_decoration.quote(
                'Некорректный формат ввода!'),
        markdown.markdown_decoration.quote(
                'Отправьте изображение.'),
        sep='\n')


def event_data_message(event_data):
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
        _
    ) = event_data
    creator = f'{creator_lname} {creator_fname}'
    date = dt.datetime.strftime(event_date, '%d.%m.%Y')
    time = dt.datetime.strftime(event_date, '%H:%M')
    pay = 'Бесплатно'
    if not event_isfree:
        pay = 'Платно'
    status = 'Действует'
    if not event_isactive:
        status = 'Не действует'
    was_sent = 'Рассылки не было'
    if event_sent:
        was_sent = 'Рассылка была'
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote('№:'),
            f'{markdown.bold(event_id)}'),
        markdown.text(
            markdown.markdown_decoration.quote('Дата события:'),
            f'{markdown.bold(date)}',),
        markdown.text(
            markdown.markdown_decoration.quote('Время события:'),
            f'{markdown.bold(time)}',),
        markdown.text(
            markdown.markdown_decoration.quote('Создал:'),
            f'{markdown.bold(creator)}'),
        markdown.text(
            markdown.markdown_decoration.quote('Телефон:'),
            f'{markdown.bold(creator_phone)}'),
        markdown.text(
            markdown.markdown_decoration.quote('Клуб:'),
            f'{markdown.bold(department)}'),
        markdown.text(
            markdown.markdown_decoration.quote('Подразделение:'),
            f'{markdown.bold(subdivision)}'),
        markdown.text(
            markdown.markdown_decoration.quote('Название:'),
            f'{markdown.bold(event_name)}'),
        markdown.text(
                markdown.markdown_decoration.quote('Описание:'),
                f'{markdown.bold(event_description)}'),
        markdown.text(
                markdown.markdown_decoration.quote('Участие:'),
                f'{markdown.bold(pay)}'),
        markdown.text(
                markdown.markdown_decoration.quote('Статус:'),
                f'{markdown.bold(status)}'),
        markdown.text(
                markdown.markdown_decoration.quote('Информирование:'),
                f'{markdown.bold(was_sent)}'),
        sep='\n')


def customers_enroll_message(data):
    if data == []:
        return markdown.text(
            markdown.markdown_decoration.quote(
                'Нет активности по мероприятию.'))
    msg = ''
    for n, user in enumerate(data, start=1):
        msg += f'{n}. {user[0]}: {user[1]}: {user[2]}\n'
    return markdown.text(
        markdown.markdown_decoration.quote(msg))


def customers_recievers_message(data):
    if data == []:
        return markdown.text(
            markdown.markdown_decoration.quote(
                'Нет активности по мероприятию.'))
    msg = ''
    for n, user in enumerate(data, start=1):
        msg += f'{n}. {user[0]}: {user[1]}: {user[2]}\n'
    return markdown.text(
        markdown.markdown_decoration.quote(msg))


def customer_event_data_message(event_data):
    (
        event_id,
        event_date,
        _,
        _,
        _,
        _,
        _,
        department,
        _,
        subdivision,
        event_name,
        event_description,
        event_isfree,
        _,
        _,
        _
    ) = event_data
    date = dt.datetime.strftime(event_date, '%d %B %Y').lower()
    time = dt.datetime.strftime(event_date, '%H:%M')
    pay = 'Бесплатно'
    if not event_isfree:
        pay = 'Платно'
    return markdown.text(
        markdown.text(
            f'🟣 {markdown.bold(event_name)}\n'),
        markdown.text(
            f'📅 {markdown.bold(date, "года в")} {markdown.bold(time)}'),
        markdown.text(
            f'🏢 {markdown.bold(department)}'),
        markdown.text(
            f'📋 {markdown.bold(subdivision)}\n'),
        markdown.text(
            f'{markdown.bold(event_description)}\n'),
        markdown.text(
            markdown.bold("₽", pay)),
        sep='\n')


""" def customer_event_data_message(event_data):
    (
        event_id,
        event_date,
        _,
        _,
        _,
        _,
        _,
        department,
        _,
        subdivision,
        event_name,
        event_description,
        event_isfree,
        _,
        _,
        _
    ) = event_data
    date = dt.datetime.strftime(event_date, '%d.%m.%Y')
    time = dt.datetime.strftime(event_date, '%H:%M')
    pay = 'Бесплатно'
    if not event_isfree:
        pay = 'Платно'
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote('№:'),
            f'{markdown.bold(event_id)}'),
        markdown.text(
            markdown.markdown_decoration.quote('Дата события:'),
            f'{markdown.bold(date)}',),
        markdown.text(
            markdown.markdown_decoration.quote('Время события:'),
            f'{markdown.bold(time)}',),
        markdown.text(
            markdown.markdown_decoration.quote('Клуб:'),
            f'{markdown.bold(department)}'),
        markdown.text(
            markdown.markdown_decoration.quote('Подразделение:'),
            f'{markdown.bold(subdivision)}'),
        markdown.text(
            markdown.markdown_decoration.quote('Название:'),
            f'{markdown.bold(event_name)}'),
        markdown.text(
                markdown.markdown_decoration.quote('Описание:'),
                f'{markdown.bold(event_description)}'),
        markdown.text(
                markdown.markdown_decoration.quote('Участие:'),
                f'{markdown.bold(pay)}'),
        sep='\n') """
