from aiogram.utils import markdown


def need_auth_message(full_name):
    if full_name is None:
        full_name = 'Гость!'
    else:
        full_name = f'{full_name}!'
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote('Здравствуйте,'),
            f'{markdown.bold(full_name)}'),
        markdown.markdown_decoration.quote(
            'Вам необходимо пройти регистрацию.'),
        markdown.text(
            markdown.markdown_decoration.quote('Нажмите на кнопку: '),
            f'{markdown.bold("Отправить контакт")}'),
        markdown.markdown_decoration.quote(
            'расположенную ниже,'),
        markdown.markdown_decoration.quote(
            'под полем ввода сообщения 🔽'),
        sep='\n')


def wrong_contact_message():
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Отправьте контакт через кнопку: '),
            f'{markdown.bold("Отправить контакт")}'),
        markdown.markdown_decoration.quote(
            'расположенную ниже,'),
        markdown.markdown_decoration.quote(
            'под полем ввода сообщения 🔽'),
        sep='\n')


def contact_recieved_message():
    return markdown.text(
        markdown.markdown_decoration.quote(
            'Контакт принят!'),
        sep='\n')


def wrong_text_message_message():
    return markdown.text(
        markdown.markdown_decoration.quote(
            'Некорректный формат ввода!'),
        markdown.markdown_decoration.quote(
            'Введите текстовое сообщение.'),
        sep='\n')


def enter_last_name_message():
    return markdown.text(
        markdown.markdown_decoration.quote(
            'Введите Вашу фамилию'),
        markdown.markdown_decoration.quote(
            'и отправьте боту.'),
        sep='\n')


def enter_first_name_message():
    return markdown.text(
        markdown.markdown_decoration.quote(
            'Далее введите имя'),
        markdown.markdown_decoration.quote(
            'и также отправьте боту.'),
        sep='\n')


def enter_patronymic_message():
    return markdown.text(
        markdown.markdown_decoration.quote(
            'Осталось указать отчество.'),
        markdown.markdown_decoration.quote(
            'Если отчество отсутствует,'),
        markdown.markdown_decoration.quote(
            'можно пропустить данный пункт.'),
        sep='\n')
