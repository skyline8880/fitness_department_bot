from aiogram.utils import markdown


def admin_menu_message(first_name, phone):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Администратор: '),
            f'{markdown.bold(first_name)}'),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Телефон: '),
            f'{markdown.bold(phone)}'),
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
            f'{markdown.bold(phone)}'),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Уже является администратором!')),
        sep='\n')


def add_admin_result_message(phone):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Номер:'),
            f'{markdown.bold(phone)}'),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Успешно добавлен как администратор!')),
        sep='\n')


def not_exist_admin_result_message(phone):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Номер:'),
            f'{markdown.bold(phone)}'),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Не является администратором!')),
        sep='\n')


def remove_admin_result_message(phone):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Номер:'),
            f'{markdown.bold(phone)}'),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Успешно удалён как администратор!')),
        sep='\n')
