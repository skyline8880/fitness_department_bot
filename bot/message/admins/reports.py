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


def period_reports_nodata(begin, end):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                f"За период: {begin} - {end}")),
        markdown.text(
            markdown.markdown_decoration.quote(
                "Нет данных!")),
        sep='\n')


def period_reports_data(begin, end):
    return markdown.text(
        markdown.markdown_decoration.quote(f'За период: {begin} - {end}'),
        markdown.markdown_decoration.quote("Отчет готов!"),
        sep='\n')
