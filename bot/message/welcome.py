from aiogram.utils import markdown


def welcome_after_auth_choose_department_message(first_name):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote('Добро пожаловать,'),
            f'{markdown.bold(first_name)}'
            f'{markdown.markdown_decoration.quote("!")}'),
        markdown.markdown_decoration.quote('На данном этапе, Вам'),
        markdown.markdown_decoration.quote('необходимо подписаться на клуб.'),
        markdown.markdown_decoration.quote('Для этого нажмите на кнопку'),
        markdown.markdown_decoration.quote('с названием клуба.\n'),
        markdown.markdown_decoration.quote('Если возникнет необходимость,'),
        markdown.markdown_decoration.quote(
            'можно отписаться, повторив нажатие.'),
        markdown.markdown_decoration.quote('При желании, можно'),
        markdown.markdown_decoration.quote('выбрать несколько клубов.\n'),
        markdown.markdown_decoration.quote('После подписки, Вам будет'),
        markdown.markdown_decoration.quote('поступать информация о'),
        markdown.markdown_decoration.quote('мероприятиях клуба.\n'),
        markdown.markdown_decoration.quote('Далее перейдите к выбору'),
        markdown.markdown_decoration.quote('подразделений.'),
        sep='\n')


def welcome_after_auth_choose_subdivision_message():
    return markdown.text(
        markdown.markdown_decoration.quote('Здесь выберите подразделения,'),
        markdown.markdown_decoration.quote(
            'в которых Вам интересны мероприятия.'),
        sep='\n')
