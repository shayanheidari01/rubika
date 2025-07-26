from collections import defaultdict, deque
from rubpy import BotClient
from rubpy.bot import filters
from rubpy.bot.models import Update
from PIL import Image  # pip install -U pillow

import os
import time
import asyncio

bot = BotClient('your-bot-token')

# داده‌های ضد اسپم
user_message_times = defaultdict(lambda: deque(maxlen=MAX_MSG_PER_WINDOW))
blocked_users = {}
notified_users = set()

# تنظیمات ضد اسپم و محدودیت‌ها
MAX_MSG_PER_WINDOW = 5
TIME_WINDOW = 10
BLOCK_DURATION = 30
MAX_MESSAGE_LENGTH = 1000

async def is_spammer(chat_id: str) -> bool:
    now = time.time()
    if chat_id in blocked_users:
        if now - blocked_users[chat_id] < BLOCK_DURATION:
            return True
        else:
            del blocked_users[chat_id]
            notified_users.discard(chat_id)
    user_message_times[chat_id].append(now)
    if len(user_message_times[chat_id]) == MAX_MSG_PER_WINDOW:
        if now - user_message_times[chat_id][0] < TIME_WINDOW:
            blocked_users[chat_id] = now
            return True
    return False

@bot.on_update(filters.commands('start'))
async def handle_start(c: BotClient, update: Update):
    if await is_spammer(update.chat_id):
        if update.chat_id not in notified_users:
            notified_users.add(update.chat_id)
            await update.reply("⛔ موقتاً بلاک شده‌اید. لطفاً چند لحظه صبر کنید.")
        return

    await update.reply(
        "🎨 سلام دوست خلاق من!\n"
        "با ارسال یک **کد رنگ هگزادسیمال** مثل `#ff5733`، می‌تونی تصویری از اون رنگ بسازی و ببینی که دقیقاً چه رنگی پشت اون کده!\n\n"
        "برای راهنمایی بیشتر، دستور `/help` رو بزن 😊"
    )

@bot.on_update(filters.commands('help'))
async def handle_help(c: BotClient, update: Update):
    if await is_spammer(update.chat_id):
        if update.chat_id not in notified_users:
            notified_users.add(update.chat_id)
            await update.reply("⛔ موقتاً بلاک شده‌اید. لطفاً چند لحظه صبر کنید.")
        return

    await update.reply(
        "🆘 راهنمای استفاده از ربات رنگ‌ساز:\n\n"
        "📌 برای ساخت تصویر رنگ دلخواه، کافیست یکی از کدهای زیر را ارسال کنی:\n"
        "`/image #ff5733`\n"
        "🔹 کد رنگ باید با `#` شروع بشه و دقیقاً 6 کاراکتر هگز داشته باشه.\n\n"
        "💡 اگر با کدهای هگز آشنایی نداری، فقط بدون که:\n"
        "`#ffffff` = سفید\n"
        "`#000000` = مشکی\n"
        "`#ff0000` = قرمز\n\n"
        "منتظرم رنگ‌های خاصت رو ببینم! 🌈"
    )

@bot.on_update(filters.commands('image'))
async def make_image(c: BotClient, update: Update):
    if await is_spammer(update.chat_id):
        if update.chat_id not in notified_users:
            notified_users.add(update.chat_id)
            await update.reply("⛔ موقتاً بلاک شده‌اید. لطفاً چند لحظه صبر کنید.")
        return

    hex_color = update.new_message.text[6:].strip()
    if not hex_color.startswith('#') or len(hex_color) != 7:
        return await update.reply("❌ فرمت رنگ اشتباه است.\n\nمثال درست:\n`/image #ff5733`")

    try:
        # تبدیل به RGB
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

        # ساخت تصویر
        file_path = f"temp_color_{hex_color[1:]}.png"
        image = Image.new('RGB', (10, 10), color=rgb)
        image.save(file_path)

        # ارسال تصویر
        await update.reply_photo(
            file_path,
            text=f"✅ تصویر رنگ `{hex_color}` آماده‌ست!\nامیدوارم خوشت بیاد 🌟"
        )

    except Exception as e:
        await update.reply(
            "⚠ در پردازش کد رنگ خطایی رخ داد.\n"
            "مثال صحیح:\n`/image #ff5733`"
        )

    finally:
        # حذف فایل پس از ارسال
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as remove_err:
                print(f"⚠ خطا در حذف فایل: {remove_err}")

bot.run()
