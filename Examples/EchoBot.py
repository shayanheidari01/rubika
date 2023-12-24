from rubpy import Client
from rubpy.types import Updates

bot = Client(
    name='name',
    # auth='auth',
    # private_key='private_key',
)
# اگه auth و private_key رو وارد کنی لاگین نمیکنه و اگه وارد نکنی با شماره لاگین میکنی.

@bot.on_message_updates()
async def updates(message: Updates):
    await message.reply('`hello` __from__ **rubpy**')

bot.run()
