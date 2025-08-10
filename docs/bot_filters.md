
# Bot Filters – `rubpy.bot.filters`

این ماژول مجموعه‌ای از **فیلترها** را برای مدیریت و فیلتر کردن آپدیت‌های ربات فراهم می‌کند.
فیلترها کلاس‌هایی هستند که متد `check` را پیاده‌سازی کرده و هنگام دریافت آپدیت، بررسی می‌کنند که آیا باید هندلر اجرا شود یا خیر.

## استفاده کلی

```python
from rubpy import BotClient
from rubpy.bot import filters

bot = BotClient("your_bot_token")

@bot.on_update(filters.text("hello"))
async def handle_hello(c, update):
    await c.send_message(update.chat_id, "Hello!")
````

---

## فهرست فیلترها

* [text](#text) – فیلتر بر اساس متن پیام
* [commands](#commands) – فیلتر برای دستورها (`/start`، `/help` و غیره)
* [update\_type](#update_type) – فیلتر بر اساس نوع آپدیت
* [private](#private) – پیام‌های چت خصوصی
* [group](#group) – پیام‌های گروه
* [bot](#bot) – پیام‌هایی که توسط ربات ارسال شده‌اند
* [chat](#chat) – فیلتر بر اساس chat\_id مشخص
* [button](#button) – کلیک دکمه (با پشتیبانی Regex)
* [forward](#forward) – پیام‌های فروارد شده
* [is\_edited](#is_edited) – پیام‌های ویرایش شده
* [sender\_type](#sender_type) – فیلتر بر اساس نوع فرستنده
* [has\_aux\_data](#has_aux_data) – وجود `aux_data` در پیام
* [file](#file) – پیام دارای فایل
* [location](#location) – پیام دارای لوکیشن
* [sticker](#sticker) – پیام دارای استیکر
* [contact\_message](#contact_message) – پیام دارای شماره تماس
* [poll](#poll) – پیام دارای نظرسنجی
* [live\_location](#live_location) – پیام دارای لوکیشن زنده

---

## `text`

فیلتر بر اساس متن پیام. پشتیبانی از **تطبیق دقیق** یا **Regex**.

```python
from rubpy.bot.filters import text

@bot.on_update(text)  # هر متنی
async def any_text(c, u):
    await u.reply("You sent some text!")

@bot.on_update(text("hello"))
async def exact(c, u):
    await u.reply("Hello!")

@bot.on_update(text(r"^/start", regex=True))
async def regex_match(c, u):
    await u.reply("Start command detected!")
```

---

## `commands`

بررسی پیام‌هایی که با دستور (مانند `/start`) شروع می‌شوند.

```python
from rubpy.bot.filters import commands

@bot.on_update(commands("start"))
async def start_cmd(c, u):
    await u.reply("Welcome!")

@bot.on_update(commands(["help", "about"]))
async def multi_cmd(c, u):
    await u.reply("Help or About!")
```

---

## `update_type`

فیلتر برای نوع خاصی از آپدیت‌ها (مثل `NewMessage`, `UpdatedMessage`, `InlineMessage`).

```python
from rubpy.bot.filters import update_type

@bot.on_update(update_type("NewMessage"))
async def new_msg(c, u):
    await u.reply("Got a new message!")

@bot.on_update(update_type(["NewMessage", "InlineMessage"]))
async def multi_type(c, u):
    await u.reply("Matched one of the update types!")
```

---

## `private`

تشخیص پیام‌های خصوصی.

```python
from rubpy.bot.filters import private

@bot.on_update(private)
async def priv(c, u):
    await u.reply("Private chat detected!")
```

---

## `group`

تشخیص پیام‌های گروهی.

```python
from rubpy.bot.filters import group

@bot.on_update(group)
async def grp(c, u):
    await u.reply("Message from group!")
```

---

## `bot`

تشخیص پیام‌هایی که توسط یک ربات ارسال شده‌اند.

```python
from rubpy.bot.filters import bot

@bot.on_update(bot)
async def from_bot(c, u):
    await u.reply("A bot sent this!")
```

---

## `chat`

اجرای هندلر فقط برای یک یا چند chat\_id مشخص.

```python
from rubpy.bot.filters import chat

@bot.on_update(chat("b0_test_chat"))
async def test_chat(c, u):
    await u.reply("Hello test chat!")

@bot.on_update(chat(["b0_admin", "b0_mod"]))
async def admin_mod(c, u):
    await u.reply("Hello admin/mod!")
```

---

## `button`

فیلتر برای کلیک دکمه‌ها، با امکان تطبیق دقیق یا Regex.

```python
from rubpy.bot.filters import button

@bot.on_update(button("btn_123"))
async def btn_123(c, u):
    await u.reply("Button 123 clicked!")

@bot.on_update(button(r"btn_\d+", regex=True))
async def numbered_btn(c, u):
    await u.reply("Numbered button clicked!")
```

---

## `forward`

تشخیص پیام‌های فروارد شده.

```python
from rubpy.bot.filters import forward

@bot.on_update(forward)
async def fwd(c, u):
    await u.reply("Forward detected!")
```

---

## `is_edited`

تشخیص پیام‌هایی که ویرایش شده‌اند.

```python
from rubpy.bot.filters import is_edited

@bot.on_update(is_edited)
async def edited_msg(c, u):
    await u.delete()
```

---

## `sender_type`

فیلتر بر اساس نوع فرستنده.

```python
from rubpy.bot.filters import sender_type

@bot.on_update(sender_type("User"))
async def from_user(c, u):
    await u.reply("Hello user!")

@bot.on_update(sender_type(["Bot", "Channel"]))
async def bot_or_channel(c, u):
    await u.reply("Hello bot or channel!")
```

---

## `has_aux_data`

تشخیص پیام‌هایی که دارای `aux_data` هستند.

```python
from rubpy.bot.filters import has_aux_data

@bot.on_update(has_aux_data)
async def aux(c, u):
    await u.reply("Has aux data")
```

---

## `file`

تشخیص پیام دارای فایل.

```python
from rubpy.bot.filters import file

@bot.on_update(file)
async def new_file(c, u):
    await u.reply("File detected!")
```

---

## `location`

تشخیص پیام دارای لوکیشن.

```python
from rubpy.bot.filters import location

@bot.on_update(location)
async def loc(c, u):
    await u.reply("Location detected!")
```

---

## `sticker`

تشخیص پیام دارای استیکر.

```python
from rubpy.bot.filters import sticker

@bot.on_update(sticker)
async def stk(c, u):
    await u.reply("Sticker detected!")
```

---

## `contact_message`

تشخیص پیام حاوی شماره تماس.

```python
from rubpy.bot.filters import contact_message

@bot.on_update(contact_message)
async def contact(c, u):
    await u.reply("Contact detected!")
```

---

## `poll`

تشخیص پیام دارای نظرسنجی.

```python
from rubpy.bot.filters import poll

@bot.on_update(poll)
async def poll_msg(c, u):
    await u.reply("Poll detected!")
```

---

## `live_location`

تشخیص پیام دارای لوکیشن زنده.

```python
from rubpy.bot.filters import live_location

@bot.on_update(live_location)
async def live_loc(c, u):
    await u.reply("Live location detected!")
```

---

---

## `multi filters`

ترکیب چند فیلتر.

```python
from rubpy.bot import filters

@bot.on_update(filters.private, filters.commands('start'))
async def multi_filter(c, u):
    await u.reply("Multi filters detected!")
```

---

## نکات تکمیلی

* همه‌ی فیلترها **async** هستند و در متد `check` بررسی انجام می‌دهند.
* می‌توان چند فیلتر را با هم ترکیب کرد.
* این فیلترها برای کار با **Update** و **InlineMessage** بهینه شده‌اند.
