
# Bot Client – `rubpy.BotClient`

کلاس **`BotClient`** هسته اصلی برای ساخت و اجرای ربات در **Rubika Bot API** است.  
این کلاس مدیریت اتصال، دریافت آپدیت‌ها، ارسال پیام و سایر عملیات API را انجام می‌دهد.

---

## ایجاد یک نمونه از BotClient

```python
from rubpy import BotClient

bot = BotClient("your_bot_token")
````

### پارامترها

| نام        | نوع   | پیش‌فرض                            | توضیح                                        |
| ---------- | ----- | ---------------------------------- | -------------------------------------------- |
| `token`    | `str` | **ضروری**                          | توکن ربات که از @BotFather روبیکا دریافت شده |
| `timeout`  | `int` | `20`                               | مدت‌زمان انتظار برای پاسخ API (ثانیه)        |
| `base_url` | `str` | `https://botapi.rubika.ir/v3/` | آدرس API (تغییر فقط در حالت تست/لوکال)       |
| `session`  | `str` | None                               | نام فایل جلسه برای ذخیره وضعیت (اختیاری)     |

---

## اجرای ربات

دو روش اصلی برای اجرای ربات وجود دارد:

### ۱. متد `run()`

این متد، رویدادهای ثبت‌شده با دکوریتور `@bot.on_update` را اجرا می‌کند و ربات را در حالت long polling نگه می‌دارد.

```python
@bot.on_update()
async def main_handler(c, update):
    await c.send_message(update.chat_id, "سلام! 👋")

bot.run()
```

---

### ۲. متد `loop()`

برای یکپارچه‌سازی با برنامه‌های async دیگر.

```python
import asyncio

async def start():
    await bot.loop()

asyncio.run(start())
```

---

## هندلرها

`BotClient` با استفاده از دکوریتور **`@bot.on_update()`** آپدیت‌ها را مدیریت می‌کند.

```python
from rubpy.bot import filters

@bot.on_update(filters.text("hello"))
async def hello_handler(c, update):
    await c.send_message(update.chat_id, "Hello there!")
```

---

### ترکیب فیلترها

می‌توان چند فیلتر را ترکیب کرد:

```python
@bot.on_update(filters.private & filters.commands("start"))
async def start_private(c, update):
    await c.send_message(update.chat_id, "Welcome to the bot!")
```

---

## متدهای کلیدی BotClient

### `send_message(chat_id, text, *, reply_to=None, buttons=None)`

ارسال پیام متنی.

```python
await bot.send_message(
    chat_id="b0_test_chat",
    text="سلام دوستان!",
    reply_to=update.message_id,
    buttons=[
        [{"text": "Button 1", "callback_data": "btn_1"}],
        [{"text": "Visit Website", "url": "https://example.com"}]
    ]
)
```

| پارامتر    | توضیح                              |
| ---------- | ---------------------------------- |
| `chat_id`  | شناسه چت (خصوصی یا گروه)           |
| `text`     | متن پیام                           |
| `reply_to` | پاسخ به یک پیام خاص (اختیاری)      |
| `buttons`  | دکمه‌های شیشه‌ای (Inline Keyboard) |

---

### `send_file(chat_id, file_path, *, caption=None)`

ارسال فایل.

```python
await bot.send_file("b0_test_chat", "photo.jpg", caption="عکس من 📷")
```

---

### `edit_message(chat_id, message_id, text, *, buttons=None)`

ویرایش پیام.

```python
await bot.edit_message("b0_test_chat", update.message_id, "متن ویرایش شده ✅")
```

---

### `delete_message(chat_id, message_id)`

حذف پیام.

```python
await bot.delete_message("b0_test_chat", update.message_id)
```

---

### `get_me()`

دریافت اطلاعات ربات.

```python
me = await bot.get_me()
print(me.username, me.first_name)
```


## توقف ربات

برای توقف امن ربات:

```python
await bot.stop()
```

یا در حالت sync:

```python
bot.stop()
```

---

## نکات مهم

* اگر از **long polling** استفاده می‌کنید، اطمینان حاصل کنید که اسکریپت همیشه در حال اجرا باشد.
* برای امنیت، توکن ربات را **در کد مستقیم ننویسید** و از متغیر محیطی استفاده کنید.
* فیلترها در `rubpy.bot.filters` ابزار قدرتمندی برای مدیریت آپدیت‌ها هستند.

---

## نمونه کامل

```python
from rubpy import BotClient
from rubpy.bot import filters

bot = BotClient("your_bot_token")

@bot.on_update(filters.commands("start"))
async def start_cmd(c, update):
    await c.send_message(update.chat_id, "Welcome to Rubpy Bot! 🚀")

@bot.on_update(filters.text())
async def echo(c, update):
    await c.send_message(update.chat_id, f"You said: {update.text}")

bot.run()
```
