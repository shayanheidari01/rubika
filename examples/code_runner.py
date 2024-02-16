from rubpy import Client, filters
from rubpy.types import Updates
from rubpy.enums import ParseMode
from runner import SourceSara
from requests import Session
from typing import List, Optional
from pydantic import BaseModel


class RunResult(BaseModel):
    output: Optional[List[str]] = None
    errors: Optional[List[str]] = None


class SourceSara:
    def __init__(self) -> None:
        self.session = Session()
        self.base_url = 'https://sourcesara.com/compiler/api'
    
    def languages(self) -> list:
        response = self.session.get(url=''.join([self.base_url, '/languages']))
        return response.json()

    def run(self, lang: str, code: str, inputs=''):
        data = dict(code=code, inputs=inputs, lang=lang)
        response = self.session.post(
            url=''.join([self.base_url, '/editor/run']),
            json=data,
            headers=dict(Origin='https://sourcesara.com')
        )
        return RunResult(**response.json())

bot = Client('bot')
source_sara = SourceSara()

@bot.on_message_updates(filters.is_group, filters.Commands('languages'))
def languages(update: Updates):
    result = ''

    get_langs = source_sara.languages()
    for lang in get_langs:
        result += ''.join(['● زبان برنامه نویسی ', lang.get('persianName'), '\n',
                           '• شناسه زبان: ', lang.get('languageId'), '\n\n'])

    return update.reply(result)

@bot.on_message_updates(filters.is_group, filters.Commands('run'))
def run_codes(update: Updates):
    code = update.raw_text[5:][len(update.command[1]):].strip()
    result = source_sara.run(update.command[1], code)
    result.output = ''.join(result.output) if result.output else None
    result.errors = ''.join(result.errors) if result.errors else None
    return update.reply(f'خروجی: \n{result.output}\n\nخطاها:\n{result.errors}')

@bot.on_message_updates(filters.is_group, filters.Commands('help'))
async def help_user(update: Updates):
    return await update.reply('دریافت زبان‌های پشتیبانی شده:\n`/languages`\n\nنحوه اجرای کد:\n\n/run python\nprint("Hello, World!")',
                        parse_mode=ParseMode.MARKDOWN)

bot.run()
