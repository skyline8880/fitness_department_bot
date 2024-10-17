from aiogram.utils import markdown


def add_reports_period_message():
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Введите период в формате: ')),
        markdown.text(
            markdown.markdown_decoration.quote(
                'ДД.ММ.ГГГГ-ДД.ММ.ГГГГ')),
        sep='\n')
