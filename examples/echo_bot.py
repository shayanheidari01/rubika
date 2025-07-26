from rubpy import BotClient
from rubpy.bot import filters

app = BotClient("bot-token")


@app.on_update(filters.text & filters.private)
async def echo(client, update):
    await update.reply(update.new_message.text)


app.run()  # Automatically start()
