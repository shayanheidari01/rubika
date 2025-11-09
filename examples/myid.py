from rubpy.bot import BotClient, filters
from rubpy.bot.models import Update

bot = BotClient('your-bot-token')

@bot.on_update(filters.commands('start'))
async def handle_start(c: BotClient, update: Update):
    if update.new_message:
        text = (
            "🆔 شناسه کاربری شما:\n{user_id}\n\n"
            "💬 شناسه چت شما:\n{chat_id}\n\n"
            "\n\n👨‍💻 سورس‌کد این ربات:\nhttps://rubpy.shayan-heidari.ir/bot_examples/#_4"
        ).format(
            user_id=update.new_message.sender_id,
            chat_id=update.chat_id
        )
        await update.reply(text)

bot.run()

