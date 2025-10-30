from rubpy.bot import BotClient, filters
from rubpy.bot.models import Update

app = BotClient("Your-Bot-Token")
GROUP_CHAT_IDS = ["group-chat-id"]
ADMIN_SENDER_ID = "your-chat-id"

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
