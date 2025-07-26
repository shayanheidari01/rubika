from rubpy import BotClient
from rubpy.bot import filters

app = BotClient("bot-token")


@app.on_update(filters.TextFilter & filters.PV)
async def echo(client, update):
    await update.reply(update.new_message.text)


import asyncio
asyncio.run(app.run())  # Automatically start()
