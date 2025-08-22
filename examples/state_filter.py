from rubpy.bot import BotClient, filters
from rubpy.bot.models import Update

app = BotClient("bot-token")

# 1) یک نمونهٔ فیلتر بساز (می‌تونی پارامترها رو تغییر بدی)
state_filter = filters.states("awaiting_email", match_mode="exact", scope="user", auto_clear=True)

@app.on_update(filters.commands("start"))
async def start(c, update: Update):
    # ست کردن state (با TTL 5 دقیقه)
    await state_filter.set_state_for(update, "awaiting_email", expire=300)
    await update.reply("لطفاً ایمیل خود را ارسال کنید.")

# 2) دستی پاک کردن (مثال)
@app.on_update(filters.commands("cancel"))
async def cancel(c, update: Update):
    await state_filter.clear_state_for(update)
    await update.reply("جریان لغو شد.")

# 3) handler ای که با state کار می‌کنه (فقط با فیلتر)
@app.on_update(state_filter)
async def got_email(c, update: Update):
    text = update.find_key("text")
    # process, validate email...
    await update.reply(f"ایمیل دریافت شد: {text}")

app.run()
