from rubpy import Client, filters
from rubpy.types import Updates
from requests import get

bot = Client('bot')

@bot.on_message_updates(filters.Commands('', prefixes='+'))
def gpt(update: Updates):
    response = get('https://api3.haji-api.ir/majid/gpt/3/free', params={'q': update.command[-1]})
    response = response.json()
    if response.get('success'):
        update.reply(response.get('result'))

bot.run()
