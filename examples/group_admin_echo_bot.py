from rubpy.bot import BotClient, filters
from rubpy.bot.models import Update

app = BotClient(
    token="BOT_TOKEN",
    rate_limit=0,
    timeout=1,)

GROUP_CHAT_IDS = ["GROUP_CHAT_ID"]
ADMIN_SENDER_ID = "ADMIN_SENDER_ID"

@app.middleware()
async def logger(bot, update, call_next):
    print("🔹 Update received:", update)
    await call_next()

@app.on_start()
async def hello(bot):
    print(await bot.get_me())
    print("Bot started!")

@app.on_update(filters.chat(GROUP_CHAT_IDS))
async def group_handler(client: BotClient, update: Update):
    if update.new_message.sender_id == ADMIN_SENDER_ID:
        if update.new_message.text:
            await update.delete()
            await client.send_message(
                chat_id=update.chat_id,
                text=update.new_message.text,
                reply_to_message_id=update.new_message.reply_to_message_id)


app.run()