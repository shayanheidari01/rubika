این بخش شامل نمونه‌های کاربردی برای کار با `rubpy` است. هر مثال یک فایل مجزا در نظر گرفته شده است.

---

## سلام دنیا

فایل: **`hello_world.py`**

```python
from rubpy import BotClient

# Create a new Client instance
app = BotClient("bot-token")


async def main():
    # Start client
    await app.start()

    # Send a message, Markdown is enabled by default
    await app.send_message("chat_id", "Hi there! I'm using **Rubpy**")

    # Close client
    await app.stop()


import asyncio
asyncio.run(main())
```

---

## دکمه های لینک دار

فایل: **`button_link.py`**

```python
"""
This source code is just a sample for rubpy.BotClient
You can edit the source code whenever you want.
"""

from rubpy import BotClient
from rubpy.bot import filters
from rubpy.bot.models import (
    ButtonLink,
    JoinChannelData,
    Update,
    Keypad,
    KeypadRow,
    Button,
)
from rubpy.bot.enums import ButtonLinkTypeEnum, ButtonTypeEnum

bot = BotClient(token="your-bot-token")


@bot.on_update(filters.commands("start"))
async def handle_start(bot, update: Update):
    keypad = Keypad(
        rows=[
            KeypadRow(
                buttons=[
                    Button(
                        id="1",
                        type=ButtonTypeEnum.LINK,
                        button_text="عضویت اجباری",
                        button_link=ButtonLink(
                            type=ButtonLinkTypeEnum.JoinChannel,
                            joinchannel_data=JoinChannelData(
                                username="rubikapy", ask_join=True
                            ),  # اگر ask_join برابر False باشد کاربر مستقیما بدون پرسش عضو کانال میشود.
                        ),
                    )
                ]
            ),
            KeypadRow(
                buttons=[
                    Button(
                        id="2",
                        type=ButtonTypeEnum.LINK,
                        button_text="باز کردن لینک",
                        button_link=ButtonLink(
                            type=ButtonLinkTypeEnum.URL,
                            link_url="https://shayan-heidari.ir/",
                        ),
                    ),
                ]
            ),
        ],
        resize_keyboard=True,
        on_time_keyboard=False,
    )

    await update.reply(
        "سلام! خوش اومدی. از دکمه‌های زیر برای کار با ربات استفاده کن:",
        inline_keypad=keypad,
    )


bot.run()
```

---

## بازتاب پیام

فایل: **`echo_bot.py`**

```python
from rubpy import BotClient
from rubpy.bot import filters
from rubpy.bot.models import Update

app = BotClient("bot-token")


@app.on_update(filters.text, filters.private)
async def echo(client, update: Update):
    await update.reply(update.new_message.text)


app.run()  # Automatically start()
```

---

## بات دریافت شناسه

فایل: **`my_chat_id.py`**

```python
from rubpy.bot import BotClient, filters
from rubpy.bot.models import Update

bot = BotClient('your-bot-token')

@bot.on_update(filters.commands('start'))
async def handle_start(c: BotClient, update: Update):
    if update.new_message:
        text = (
            "🆔 شناسه کاربری شما:\n{user_id}\n\n"
            "💬 شناسه چت شما:\n{chat_id}\n\n"
        ).format(
            user_id=update.new_message.sender_id,
            chat_id=update.chat_id
        )
        await update.reply(text)

bot.run()
```

---

## استفاده از states

فایل: **`state_filter.py`**

```python
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
```


---

## یک مثال از میان افزار

فایل: **`middleware_example.py`**

### ترتیب اجرای Middleware ها
هر آپدیت جدیدی که بیاد، این مسیر رو طی می‌کنه:

1. `logger` → همیشه لاگ می‌گیره.
2. `auth_checker` → اگه کاربر غیرمجاز باشه، مسیر قطع می‌شه.
3. `rate_limiter` → اگه اسپم باشه، قطع می‌شه.
4. در نهایت می‌ره به `main_handler`.

```python
from rubpy.bot import BotClient, filters
from rubpy.bot.models import Update, InlineMessage
from collections import defaultdict
import time

user_timestamps = defaultdict(float)

bot = BotClient("your-bot-token")


# 🔹 Middleware 1: Logger
@bot.middleware()
async def logger(bot, update, call_next):
    """
    Logs every update before it reaches the handlers.
    """
    update_type = "InlineMessage" if isinstance(update, InlineMessage) else update.type
    user_id = getattr(update, "chat_id", None)
    print(f"📥 [Logger] type={update_type}, user={user_id}")
    await call_next()  # ادامه بده به middleware بعدی یا handler


# 🔹 Middleware 2: Auth Checker
@bot.middleware()
async def auth_checker(bot, update, call_next):
    """
    Blocks users that are not in allowed list.
    """
    allowed_users = {"b0IYdTF0EWT0d3c486d5205d051e86c5"}  # فقط این کاربرا مجازن
    user_id = getattr(update, "chat_id", None)

    if user_id not in allowed_users:
        print(f"🚫 [Auth] کاربر {user_id} اجازه دسترسی نداره")
        return  # نذار به هندلر برسه

    await call_next()


# 🔹 Middleware 3: Rate Limiter
@bot.middleware()
async def rate_limiter(bot, update, call_next):
    """
    Prevents users from spamming (1 message per 3 seconds).
    """
    user_id = getattr(update, "chat_id", None)
    now = time.time()

    if user_id and now - user_timestamps[user_id] < 3:
        print(f"⚠️ [RateLimit] کاربر {user_id} داره اسپم می‌کنه")
        return

    user_timestamps[user_id] = now
    await call_next()


# 🔹 Handler
@bot.on_update(filters.text)
async def main_handler(bot, update: Update):
    print(f"✅ Handler: پیام دریافت شد → {update.chat_id}")
    await update.reply("پیام شما دریافت شد ✅")


bot.run()

```

### نکته‌ها

* اگه **هیچکدوم** `return` نکنن، همه اجرا می‌شن و در نهایت می‌ره به هندلر.
* می‌تونی middleware ها رو برای **تست A/B، cache، ترجمه متن، حتی اضافه کردن context به آپدیت** استفاده کنی.
* ترتیب ثبت شدن (`@bot.middleware()`) مهمه؛ همون ترتیبی که نوشتی، اجرا می‌شن.