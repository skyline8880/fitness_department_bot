from aiogram.utils import markdown


def action_message(action):
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Активность: '),
            f'{markdown.bold(action)}'),
        sep='\n')
