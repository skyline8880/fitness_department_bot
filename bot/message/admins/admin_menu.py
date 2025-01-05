from aiogram.utils import markdown


def admin_menu_message(
        first_name,
        phone,
        clubs,
        subdivs):
    user_clubs = ''
    for cl in clubs:
        user_clubs += f'➤ {cl}\n'
    need_msg = ''
    if clubs == []:
        user_clubs = (
            '➖ нет ни одного клуба\n')
        ch_sb = 'выбранному подразделению'
        if len(subdivs) > 1:
            ch_sb = 'выбранным подразделениям'
        need_msg = (
            'Необходимо выбрать, хотя бы\n'
            'один клуб и получать информацию\n'
            'о мероприятиях в нём, по\n'
            f'{ch_sb}.\n')
    user_subdivs = ''
    for sub in subdivs:
        user_subdivs += f'➤ {sub}\n'
    if subdivs == []:
        user_subdivs = (
            '➖ нет ни одного подразделения\n')
        ch_cl = 'выбранном клубе'
        if len(clubs) > 1:
            ch_cl = 'выбранных клубах'
        need_msg = (
            'Необходимо выбрать, хотя бы\n'
            'одно подразделение и получать\n'
            'информацию о мероприятиях\n'
            f'по нему, в {ch_cl}.\n')
    if clubs == [] and subdivs == []:
        need_msg = (
            'Необходимо выбрать хотя бы\n'
            'один клуб и одно подразделение,\n'
            'чтобы получать информацию\n'
            'о мероприятиях подразделения\n'
            'в клубе.\n')
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Администратор: '),
            f'{markdown.bold(first_name)}'),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Телефон: '),
            f'{markdown.code(phone)}\n'),
        markdown.markdown_decoration.quote('Клубы:'),
        markdown.markdown_decoration.quote(user_clubs),
        markdown.markdown_decoration.quote('Подразделения:'),
        markdown.markdown_decoration.quote(user_subdivs),
        markdown.markdown_decoration.quote(need_msg),
        sep='\n')


def add_remove_admin_message(action):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Активность: '),
            f'{markdown.bold(action)}'),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Введите номер телефона:'),
            f'{markdown.bold("7xxxxxxxxxx")}'),
        sep='\n')


def wrong_admin_phone_message():
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Введите номер корректно!')),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Сообщение должно содержать')),
        markdown.text(
            markdown.markdown_decoration.quote(
                'только цифры.')),
        sep='\n')


def exist_admin_result_message(phone):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Номер:'),
            f'{markdown.code(phone)}'),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Уже является администратором!')),
        sep='\n')


def add_admin_result_message(phone):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Номер:'),
            f'{markdown.code(phone)}'),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Успешно добавлен как администратор!')),
        sep='\n')


def not_exist_admin_result_message(phone):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Номер:'),
            f'{markdown.code(phone)}'),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Не является администратором!')),
        sep='\n')


def remove_admin_result_message(phone):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Номер:'),
            f'{markdown.code(phone)}'),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Успешно удалён как администратор!')),
        sep='\n')
