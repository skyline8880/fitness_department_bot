from aiogram.utils import markdown


def user_menu_message(
        last_name,
        first_name,
        clubs,
        subdivs):
    user_fullname = f'{last_name} {first_name}'
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
            markdown.markdown_decoration.quote('Пользователь:'),
            f'{markdown.bold(user_fullname)}\n'),
        markdown.markdown_decoration.quote('Клубы:'),
        markdown.markdown_decoration.quote(user_clubs),
        markdown.markdown_decoration.quote('Подразделения:'),
        markdown.markdown_decoration.quote(user_subdivs),
        markdown.markdown_decoration.quote(need_msg),
        markdown.markdown_decoration.quote('────────────────'),
        markdown.markdown_decoration.quote('Перейти к выбору клубов'),
        markdown.markdown_decoration.quote('и подразделений ▼'),
        sep='\n')


def user_choose_depart_message():
    return markdown.text(
        markdown.markdown_decoration.quote('Выберите один или'),
        markdown.markdown_decoration.quote('несколько клубов'),
        sep='\n')


def user_choose_subdiv_message():
    return markdown.text(
        markdown.markdown_decoration.quote('Выберите одно или'),
        markdown.markdown_decoration.quote('несколько подразделений'),
        sep='\n')
