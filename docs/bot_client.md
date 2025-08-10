
# 📘 مستندات کلاس `BotClient` — کتابخانه `rubpy`

> **منبع:** بر اساس کد منبع (`bot.py`) و بازخوردهای جامعه توسعه‌دهندگان  
> **هدف:** راهنمای جامع و نهایی برای تعامل با **Rubika Bot API** (`https://botapi.rubika.ir/v3/<token>/`)  

---

## 🌟 خلاصه و هدف

کلاس `BotClient` هسته اصلی کتابخانه `rubpy` است و یک رابط ناهمگام (async) برای ساخت بات‌های هوشمند در پلتفرم **Rubika** فراهم می‌کند. این کلاس تمام ابزارهای لازم برای توسعه بات‌های پیچیده و مقیاس‌پذیر را در اختیار شما قرار می‌دهد.

### ✅ قابلیت‌های کلیدی:
- پشتیبانی از **Polling** و **Webhook** برای دریافت آپدیت
- ثبت هندلرهای هوشمند با **فیلترهای قدرتمند**
- ارسال انواع محتوا: پیام، فایل، استیکر، نظرسنجی، موقعیت، مخاطب
- مدیریت کیبوردهای چت و دکمه‌های تعاملی
- آپلود و دانلود فایل با پشتیبانی از **پیشرفت عملیات**
- محدودیت نرخ داخلی برای جلوگیری از بلاک شدن
- ایمنی در همزمانی با پشتیبانی از هندلرهای همگام و ناهمگام

---

## 🛠️ پیش‌نیازها

### 🔧 وابستگی‌ها
- **پایتون:** ۳.۸+
- **کتابخانه‌ها:**
- `aiohttp` — برای درخواست‌های HTTP ناهمگام
- `rubpy` — کتابخانه اصلی
- **توکن بات:** از ربات @BotFather دریافت کنید

### 📦 نصب
```bash
pip install -U rubpy
```

### 📥 وارد کردن ماژول‌ها
```python
import asyncio
from typing import Optional
from rubpy import BotClient
from rubpy.bot import filters
from rubpy.bot.enums import UpdateTypeEnum, ChatKeypadTypeEnum
from rubpy.bot.models import Keypad, Update
```

---

## 🏗️ معماری کلی

`BotClient` یک ساختار ناهمگام و رویدادمحور دارد که بر پایه `asyncio` و `aiohttp` ساخته شده است.

### 🔁 مدل‌های دریافت آپدیت

| مدل | توضیح | پیشنهاد |
|-----|------|--------|
| **Polling** | دریافت دوره‌ای آپدیت از سرور | مناسب برای توسعه و تست |
| **Webhook** | ارسال آپدیت توسط سرور به URL شما | مناسب برای محیط تولید |

### 🔄 چرخه پردازش آپدیت:
1. دریافت داده خام از API
2. تحلیل به شیء `Update` یا `InlineMessage`
3. فیلتر پیام‌های قدیمی (بیش از ۵ ثانیه)
4. جلوگیری از پردازش تکراری با `processed_messages`
5. اجرای هندلرهای متناسب با فیلترها

---

## 🧱 مدل‌های کلیدی

مدل‌ها با استفاده از `dataclass` پیاده‌سازی شده‌اند و داده‌ها را به صورت ساختاریافته مدیریت می‌کنند.

| مدل | توضیح |
|-----|-------|
| `Update` | شامل نوع آپدیت، شناسه چت، پیام جدید/ویرایش‌شده/حذف‌شده |
| `InlineMessage` | پیام‌های ارسالی از طریق دکمه‌های تعاملی |
| `Message` | ساختار کامل پیام (متن، زمان، فایل، و غیره) |
| `MessageId` | شناسه پیام و فایل |
| `Keypad` | کیبورد چت یا دکمه‌های inline |

### 🔤 enumهای مهم:
- `UpdateTypeEnum`: `NEW_MESSAGE`, `UPDATED_MESSAGE`, `REMOVED_MESSAGE`
- `ChatKeypadTypeEnum`: `NONE`, `NEW`, `REPLACE`, `REMOVE`

---

## 🚀 شروع به کار

### ساخت نمونه
```python
client = BotClient(
    token="YOUR_BOT_TOKEN",
    rate_limit=0.5,          # تأخیر بین درخواست‌ها (ثانیه)
    use_webhook=False        # True برای وبهوک
)
```

### مدیریت چرخه عمر
```python
await client.start()   # شروع جلسه
await client.run()     # اجرای بات (Polling یا Webhook)
await client.stop()    # پایان جلسه
```

---

## 📡 متدهای اصلی

### 📥 ارسال محتوا
| متد | توضیح |
|------|--------|
| `send_message(chat_id, text)` | ارسال پیام متنی |
| `send_sticker(chat_id, sticker_id)` | ارسال استیکر |
| `send_file(chat_id, file, type)` | ارسال فایل (تصویر، صدا، ویدیو و ...) |
| `send_poll(chat_id, question, options)` | ارسال نظرسنجی |
| `send_location(chat_id, lat, lon)` | ارسال موقعیت جغرافیایی |
| `send_contact(chat_id, first, last, phone)` | ارسال مخاطب |

### 🔄 مدیریت پیام
| متد | توضیح |
|------|--------|
| `edit_message_text(chat_id, msg_id, text)` | ویرایش متن پیام |
| `delete_message(chat_id, msg_id)` | حذف پیام |
| `forward_message(from_id, msg_id, to_id)` | فوروارد پیام |

### 📁 مدیریت فایل
| متد | توضیح |
|------|--------|
| `request_send_file(type)` | دریافت آدرس آپلود |
| `upload_file(url, path, name)` | آپلود فایل |
| `get_file(file_id)` | دریافت لینک دانلود |
| `download_file(file_id, save_as, progress)` | دانلود با پیشرفت |

### 🌐 وبهوک
```python
await client.run(
    webhook_url="https://your-domain.com/bot",
    path="/bot",
    host="0.0.0.0",
    port=8080
)
```

---

## 🎯 ثبت هندلرها

با استفاده از دکوراتور `@on_update` و فیلترها، رویدادها را مدیریت کنید:

```python
@client.on_update(filters.commands("start"))
async def welcome(client, update):
    await update.reply("سلام! به بات خوش آمدید.")
```

### فیلترهای پیش‌ساخته:
- `filters.text` — فقط پیام‌های متنی
- `filters.photo` — تصاویر
- `filters.private` — چت خصوصی
- `filters.group` — گروه
- `filters.commands("start")` — دستورات خاص

### فیلتر سفارشی:
```python
class ContainsHelloFilter(filters.Filter):
    async def check(self, update):
        return "سلام" in (update.new_message.text or "")
```

---

## ⚙️ بهترین شیوه‌ها

1. **مدیریت جلسه:** همیشه از `try/finally` استفاده کنید.
2. **محدودیت نرخ:** در بات‌های پرکاربر، `rate_limit=1` تنظیم کنید.
3. **SSL:** در تولید، `ssl=True` را فعال کنید.
4. **لاگ‌گیری:** برای دیباگ، `logging.DEBUG` را فعال کنید.
5. **وبهوک:** از دامنه HTTPS و سرور پایدار استفاده کنید.

---

## 🐞 مدیریت خطاها

### خطاهای رایج:
- `ClientResponseError` — مشکل در ارتباط با API
- `ValueError` — پارامتر نامعتبر
- `JSONDecodeError` — داده نامعتبر در Webhook

### فعال‌سازی لاگ:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🧪 مثال‌های کاربردی

### ۱. بات ساده با کیبورد
```python
from rubpy import BotClient
from rubpy.bot import filters
from rubpy.bot.models import Keypad, KeypadRow, Button

client = BotClient("TOKEN")

@client.on_update(filters.commands("start"))
async def start(client, update):
    keypad = Keypad(
        rows=[KeypadRow(buttons=[Button(id="1", button_text="شروع")])],
        resize_keyboard=True
    )
    await update.reply("به بات خوش آمدید!", chat_keypad=keypad)

client.run()
```

### ۲. بات وبهوک
```python
await client.run(webhook_url="https://example.com/bot", path="/bot")
```

### ۳. دانلود فایل با پیشرفت
```python
def progress(downloaded, total):
    print(f"دریافت: {downloaded}/{total} بایت")

await client.download_file("file123", "photo.jpg", progress=progress)
```

---

## ❓ سوالات متداول

**س: چرا آپدیت‌ها دریافت نمی‌شوند؟**  
ج: مطمئن شوید `has_time_passed` فعال است یا لاگ را در سطح `DEBUG` بررسی کنید.

**س: چطور فیلتر سفارشی بنویسم؟**  
ج: یک کلاس از `filters.Filter` ارث‌بری کنید و متد `check` را پیاده‌سازی کنید.

**س: آیا آپلود تکه‌تکه (chunked) پشتیبانی می‌شود؟**  
ج: خیر، اما در آینده اضافه خواهد شد.

---

## 📎 پیوست: مثال پیشرفته

### بات با فیلتر سفارشی و هندلر همگام
```python
class GreetingFilter(filters.Filter):
    async def check(self, update):
        text = update.new_message.text or ""
        return any(word in text.lower() for word in ["سلام", "های", "hello"])

@app.on_update(GreetingFilter())
def greet_sync(client, update):
    update.reply("درود! چطوری؟")
```
---

**طراحی شده با ❤️ برای توسعه‌دهندگان فارسی‌زبان** 

