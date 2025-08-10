# مستندات کلاس `BotClient` — کتابخانه `rubpy`

> **نسخه مستندات:** ۳.۰ (آخرین به‌روزرسانی: مرداد ۱۴۰۴)\
> **توضیح کلی:** این مستندات، راهنمای جامع و نهایی کلاس `BotClient` در کتابخانه `rubpy` است که برای تعامل با **Rubika Bot API** (`https://botapi.rubika.ir/v3/<token>/`) طراحی شده است. این سند بر اساس کد منبع (`bot.py`) و بازخورد کاربران تهیه شده و شامل توضیحات دقیق متدها، مدل‌ها، فیلترها، الگوهای همزمانی، مدیریت خطاها، و مثال‌های کاربردی است. هدف، ارائه راهنمایی کامل برای توسعه‌دهندگان بات‌های Rubika با تمرکز بر خوانایی، دقت، و بهترین شیوه‌ها است.

---

## فهرست مطالب

- خلاصه و هدف
- پیش‌نیازها
- معماری و رفتار کلی
- مدل‌های کلیدی
- نمونه‌سازی `BotClient`
- متدهای اصلی
  - مدیریت جلسه و چرخه عمر
  - مدیریت درخواست‌ها و محدودیت نرخ
  - اطلاعات حساب و چت
  - ارسال محتوا
  - آپلود و دانلود فایل
  - دریافت و پردازش آپدیت‌ها
  - مدیریت پیام‌ها و چت
  - مدیریت وبهوک
  - توابع کمکی
- ثبت هندلرها و فیلترها
- الگوی همزمانی و ایمنی
- بهترین شیوه‌ها
- مدیریت خطاها و دیباگ
- مثال‌های کاربردی
- سوالات متداول (FAQ)
- محدودیت‌ها و پیشنهادات
- پیوست: مثال‌های پیشرفته

---

## خلاصه و هدف

کلاس `BotClient` در کتابخانه `rubpy` یک کلاینت ناهمگام (async) برای تعامل با **Rubika Bot API** است. این کلاس برای توسعه‌دهندگان بات‌های Rubika طراحی شده و قابلیت‌های زیر را ارائه می‌دهد:

- **پشتیبانی از Polling و Webhook:** دریافت آپدیت‌ها از طریق پرس‌وجو دوره‌ای یا سرور webhook.
- **هندلرهای مبتنی بر فیلتر:** ثبت هندلرها با دکوراتور `on_update` و فیلترهای سفارشی.
- **عملیات متنوع:** ارسال پیام، استیکر، فایل، نظرسنجی، موقعیت جغرافیایی، و مخاطب؛ ویرایش/حذف پیام‌ها؛ مدیریت کیبوردها.
- **مدیریت فایل:** آپلود و دانلود فایل با پشتیبانی از پیشرفت دانلود.
- **محدودیت نرخ داخلی:** جلوگیری از بلاک شدن توسط API با تأخیر قابل تنظیم.
- **همزمانی ایمن:** پشتیبانی از هندلرهای sync و async با استفاده از `asyncio` و `threading`.

این مستندات برای توسعه‌دهندگان مبتدی تا حرفه‌ای مناسب است و شامل مثال‌های تست‌شده برای سناریوهای واقعی است.

---

## پیش‌نیازها

### وابستگی‌ها

- **پایتون:** نسخه ۳.۸ یا بالاتر
- **کتابخانه‌ها:**
  - `aiohttp`: برای درخواست‌های HTTP ناهمگام
  - `rubpy`: کتابخانه اصلی (شامل مدل‌ها و فیلترها)
  - استاندارد پایتون: `asyncio`, `logging`, `mimetypes`, `collections.deque`, `uuid`
- **توکن بات:** توکن معتبر از Rubika Bot API

### نصب

```bash
pip install aiohttp rubpy
```

### وارد کردن ماژول‌ها

```python
import asyncio
import aiohttp
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Literal, Optional, Union, Tuple
from rubpy import BotClient
from rubpy.bot.enums import ChatKeypadTypeEnum, UpdateTypeEnum
from rubpy.bot.filters import Filter
from rubpy.bot.models import Keypad, InlineMessage, Update, Message, MessageId, Bot, Chat
```

---

## معماری و رفتار کلی

- **ساختار پایه:** `BotClient` با دریافت `token`، پایه URL (`https://botapi.rubika.ir/v3/<token>/`) را تنظیم می‌کند. پارامتر `use_webhook` حالت اولیه (Polling یا Webhook) را مشخص می‌کند.
- **ارتباط با API:** درخواست‌ها از طریق `_make_request` (POST با JSON) ارسال می‌شوند. محدودیت نرخ با `_rate_limit_delay` اعمال می‌شود.
- **دریافت آپدیت‌ها:**
  - **Polling:** حلقه در `run` که `updater` را فراخوانی می‌کند؛ آپدیت‌های قدیمی (&gt;۵ ثانیه) فیلتر می‌شوند.
  - **Webhook:** سرور `aiohttp` راه‌اندازی شده و endpointها با `update_bot_endpoints` ثبت می‌شوند.
- **پردازش آپدیت‌ها:** `_parse_update` داده‌های خام را به `Update` یا `InlineMessage` تبدیل می‌کند؛ `process_update` هندلرهای منطبق را اجرا می‌کند.
- **ایمنی:** `processed_messages` (یک deque با `maxlen=10000`) از پردازش تکراری پیام‌ها جلوگیری می‌کند (به جز InlineMessage).
- **لاگ‌گیری:** استفاده از `logging` با سطوح INFO، DEBUG، ERROR، و EXCEPTION.

**جدول مقایسه مدل‌های دریافت آپدیت:**

| مدل | مزایا | معایب | استفاده پیشنهادی |
| --- | --- | --- | --- |
| Polling | ساده، بدون نیاز به سرور خارجی | مصرف منابع بالا (پرس‌وجو مداوم) | توسعه محلی، بات‌های کوچک |
| Webhook | کارآمد، بلادرنگ | نیاز به URL عمومی و HTTPS | تولید، بات‌های بزرگ |

---

## مدل‌های کلیدی

مدل‌ها با `dataclasses` پیاده‌سازی شده‌اند. خلاصه فیلدها:

- `Update`:

  - `type`: از `UpdateTypeEnum` (NEW_MESSAGE, UPDATED_MESSAGE, REMOVED_MESSAGE)
  - `chat_id`: شناسه چت
  - `new_message`/`updated_message`: شیء `Message` (اختیاری)
  - `removed_message_id`: شناسه پیام حذف‌شده
  - `client`: مرجع به `BotClient`

- `InlineMessage`:

  - `sender_id`, `text`, `message_id`, `chat_id`
  - `file`, `location`, `aux_data`: داده‌های اضافی
  - `client`: مرجع به `BotClient`

- `Message`:

  - `message_id`, `text`, `time`, و غیره (جزئیات در مدل پروژه)

- `MessageId`:

  - `chat_id`, `message_id`, `file_id` (اختیاری), `client`

- `Keypad`:

  - `rows`: لیست `KeypadRow` (هر کدام شامل `Button`)
  - `resize_keyboard`, `on_time_keyboard`: تنظیمات نمایش

- `Bot`**,** `Chat`: اطلاعات بات و چت (از `get_me`, `get_chat`)

**Enumها:**

- `ChatKeypadTypeEnum`: NONE, NEW, REPLACE, REMOVE
- `UpdateTypeEnum`: NEW_MESSAGE, UPDATED_MESSAGE, REMOVED_MESSAGE

---

## نمونه‌سازی `BotClient`

```python
from rubpy import BotClient

client = BotClient(
    token="YOUR_BOT_TOKEN",
    rate_limit=0.5,      # تأخیر بین درخواست‌ها (ثانیه)
    use_webhook=False    # False برای Polling، True برای Webhook
)
```

**پارامترها:**

- `token` (str): توکن بات (اجباری).
- `rate_limit` (float): حداقل تأخیر بین درخواست‌ها (پیش‌فرض ۰.۵).
- `use_webhook` (bool): انتخاب حالت اولیه (در `run` قابل override).

---

## متدهای اصلی

### مدیریت جلسه و چرخه عمر

- `async def start(self) -> None`:

  - ایجاد `aiohttp.ClientSession` و تنظیم `running = True`.
  - مثال: `await client.start()`

- `async def stop(self) -> None`:

  - بستن جلسه و تنظیم `running = False`.
  - مثال: `await client.stop()`

- `async def run(self, webhook_url: Optional[str] = None, path: Optional[str] = '/webhook', host: str = "0.0.0.0", port: int = 8080) -> None`:

  - اجرا در حالت Polling (بدون `webhook_url`) یا Webhook (با سرور aiohttp).

  - Polling: حلقه با تأخیر ۰.۱ ثانیه؛ خطاها با تأخیر ۲ ثانیه retry می‌شوند.

  - Webhook: ثبت endpointها با `update_bot_endpoints`.

  - مثال:

    ```python
    # Polling
    await client.run()
    # Webhook
    await client.run(webhook_url="https://example.com", path="/bot")
    ```

- `async def close(self) -> None`:

  - بستن جلسه (مشابه `stop`).

### مدیریت درخواست‌ها و محدودیت نرخ

- `async def _rate_limit_delay(self) -> None`:

  - داخلی: صبر تا `rate_limit` ثانیه از درخواست قبلی.

- `async def _make_request(self, method: str, data: Dict) -> Dict`:

  - ارسال POST با JSON؛ چک `status=='OK'`.
  - بازگشت: `data` یا `{"status": "ERROR", "error": ...}`.
  - خطاها: `aiohttp.ClientResponseError` لاگ می‌شود.

### اطلاعات حساب و چت

- `async def get_me(self) -> Bot`:

  - بازگشت اطلاعات بات.
  - مثال: `bot_info = await client.get_me(); print(bot_info.username)`

- `async def get_chat(self, chat_id: str) -> Chat`:

  - بازگشت اطلاعات چت.
  - مثال: `chat = await client.get_chat("chat123"); print(chat.title)`

### ارسال محتوا

- `async def send_message(self, chat_id: str, text: str, chat_keypad: Optional[Keypad] = None, inline_keypad: Optional[Keypad] = None, disable_notification: bool = False, reply_to_message_id: Optional[str] = None, chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE) -> MessageId`:

  - ارسال پیام متنی با کیبورد.
  - مثال: `await client.send_message("chat123", "Hello!")`

- `async def send_sticker(self, chat_id: str, sticker_id: str, ...) -> MessageId`:

  - مشابه `send_message` با `sticker_id`.

- `async def send_file(self, chat_id: str, file: Optional[Union[str, Path]] = None, file_id: Optional[str] = None, text: Optional[str] = None, file_name: Optional[str] = None, type: Literal['File', 'Image', 'Voice', 'Music', 'Gif', 'Video'] = 'File', ...) -> MessageId`:

  - آپلود فایل (اگر `file` داده شود) و ارسال با `file_id`.
  - مثال: `await client.send_file("chat123", file="image.png", type="Image")`

- `async def send_poll(self, chat_id: str, question: str, options: List[str]) -> MessageId`:

  - ارسال نظرسنجی.

- `async def send_location(self, chat_id: str, latitude: Union[str, float], longitude: Union[str, float], ...) -> MessageId`:

  - ارسال موقعیت.

- `async def send_contact(self, chat_id: str, first_name: str, last_name: str, phone_number: str, ...) -> MessageId`:

  - ارسال مخاطب.

### آپلود و دانلود فایل

- `async def request_send_file(self, type: Literal['File', 'Image', 'Voice', 'Music', 'Gif', 'Video']) -> str`:

  - بازگشت `upload_url`.
  - خطا: `ValueError` برای `type` نامعتبر.

- `async def upload_file(self, url: str, file_name: str, file_path: str) -> str`:

  - آپلود فایل با `aiohttp.FormData`.
  - هشدار: `ssl=False` در کد (برای تولید `ssl=True` کنید).
  - بهبود پیشنهادی: استفاده از `with open(...)`.

- `async def get_file(self, file_id: str) -> str`:

  - بازگشت `download_url`.

- `async def download_file(self, file_id: str, save_as: Optional[str] = None, progress: Optional[Callable[[int, int], None]] = None, chunk_size: int = 65536, as_bytes: bool = False) -> Union[str, bytes, None]`:

  - دانلود با پشتیبانی از progress callback.

  - مثال:

    ```python
    def prog(d, t): print(f"{d}/{t} bytes")
    await client.download_file("file123", "out.jpg", progress=prog)
    ```

### دریافت و پردازش آپدیت‌ها

- `async def get_updates(self, limit: int = 100, offset_id: str = "") -> List[Union[Update, InlineMessage]]`:

  - دریافت فوری آپدیت‌ها (فقط برای REMOVED_MESSAGE).

- `async def updater(self, limit: int = 100, offset_id: str = "") -> List[Union[Update, InlineMessage]]`:

  - مدیریت `next_offset_id`؛ فیلتر پیام‌های قدیمی (&gt;۵ ثانیه).

- `def _parse_update(self, item: Dict) -> Optional[Union[Update, InlineMessage]]`:

  - تبدیل دیکشنری به `Update` یا `InlineMessage`.

- `async def process_update(self, update: Union[Update, InlineMessage]) -> None`:

  - اجرای هندلرهای منطبق با فیلترها.

- `async def _filters_pass(self, update: Union[Update, InlineMessage], filters: Tuple[Filter, ...]) -> bool`:

  - چک async فیلترها.

- `def on_update(self, *filters: Filter) -> Callable`:

  - دکوراتور برای ثبت هندلرها.

### مدیریت پیام‌ها و چت

- `async def forward_message(self, from_chat_id: str, message_id: str, to_chat_id: str, disable_notification: bool = False) -> MessageId`:

  - فوروارد پیام.

- `async def edit_message_text(self, chat_id: str, message_id: str, text: str) -> bool`:

  - ویرایش متن پیام.

- `async def edit_message_keypad(self, chat_id: str, message_id: str, inline_keypad: Keypad) -> bool`:

  - ویرایش کیبورد inline.

- `async def delete_message(self, chat_id: str, message_id: str) -> bool`:

  - حذف پیام.

- `async def set_commands(self, commands: List[Dict[str, str]]) -> bool`:

  - تنظیم دستورات بات (مثل `/start`).

- `async def edit_chat_keypad(self, chat_id: str, keypad_type: ChatKeypadTypeEnum, keypad: Optional[Keypad] = None) -> bool`:

  - ویرایش کیبورد چت.

- `async def update_bot_endpoints(self, url: str, endpoint_type: str) -> Any`:

  - ثبت endpoint برای Webhook.

### مدیریت وبهوک

- `async def handle_webhook(self, request: web.Request) -> web.Response`:
  - پردازش درخواست‌های Webhook؛ بازگشت JSON `{"status": "OK"}` یا خطا (۴۰۰/۵۰۰).

### توابع کمکی

- `def _extract_message_id(self, update: Union[Update, InlineMessage]) -> Optional[str]`:

  - استخراج `message_id` برای جلوگیری از پردازش تکراری.

- `def has_time_passed(last_time, seconds: int = 5) -> bool`:

  - چک زمان پیام.

- `def get_extension(content_type: str) -> str`:

  - بازگشت پسوند فایل از MIME type.

---

## ثبت هندلرها و فیلترها

هندلرها با دکوراتور `on_update` ثبت می‌شوند:

```python
@client.on_update(filters.commands("start"))
async def handle_start(client: BotClient, update: Update):
    await update.reply("Welcome!")
```

- **فیلترها:** کلاس‌هایی با متد `async def check(self, update) -> bool`. مثال: `filters.text`, `filters.commands`.
- **ترکیب:** از `,` برای ترکیب فیلترها (مثل `filters.text, filters.private`).
- **نمونه‌سازی:** اگر کلاس فیلتر ارسال شود، در زمان چک نمونه‌سازی می‌شود.

---

## الگوی همزمانی و ایمنی

- **هندلرها:**
  - Async: با `asyncio.create_task` اجرا می‌شوند.
  - Sync: در `threading.Thread` جداگانه برای جلوگیری از بلاک شدن.
- **ایمنی:** `processed_messages` از پردازش تکراری جلوگیری می‌کند (به جز InlineMessage).
- **هشدار:** برای هندلرهای سنگین، از queue یا worker pool استفاده کنید.

---

## بهترین شیوه‌ها

1. **مدیریت جلسه:** همیشه `await client.start()` و `await client.stop()` را در `try-finally` قرار دهید.
2. **فایل‌ها:** در `upload_file` از `with open(...) as f` استفاده کنید.
3. **SSL:** `ssl=False` را در تولید حذف کنید.
4. **Rate Limit:** برای بات‌های بزرگ، `rate_limit` را به ۱+ ثانیه تنظیم کنید.
5. **فیلتر پیام‌های قدیمی:** `has_time_passed` را تنظیم کنید.
6. **Webhook:** از HTTPS و سرور پایدار استفاده کنید.
7. **لاگ‌گیری:** سطح DEBUG را برای توسعه فعال کنید.

---

## مدیریت خطاها و دیباگ

- **لاگ‌گیری:** فعال‌سازی با:

  ```python
  logging.basicConfig(level=logging.DEBUG)
  ```

- **خطاهای رایج:**

  - `aiohttp.ClientResponseError`: مشکل در پاسخ API (چک status).
  - `ValueError`: پارامترهای نامعتبر (مثل `type` در `request_send_file`).
  - `json.JSONDecodeError`: در Webhook برای JSON نامعتبر.

- **دیباگ:** لاگ‌های "API response" و "Failed to parse" را بررسی کنید.

---

## مثال‌های کاربردی

### ۱. بات Polling ساده با کیبورد

```python
import asyncio
import logging
from rubpy import BotClient
from rubpy.bot import filters
from rubpy.bot.models import Keypad, KeypadRow, Button
from rubpy.bot.enums import ChatKeypadTypeEnum

logging.basicConfig(level=logging.INFO)

async def main():
    client = BotClient("YOUR_BOT_TOKEN", rate_limit=0.5)
    await client.start()

    @client.on_update(filters.commands("start"))
    async def handle_start(client, update):
        keypad = Keypad(
            rows=[KeypadRow(buttons=[Button(id="1", type="Simple", button_text="Click Me")])],
            resize_keyboard=True
        )
        await update.reply("Welcome!", chat_keypad=keypad, chat_keypad_type=ChatKeypadTypeEnum.NEW)

    try:
        await client.run()
    finally:
        await client.stop()

asyncio.run(main())
```

### ۲. بات Webhook

```python
async def main():
    client = BotClient("YOUR_BOT_TOKEN", use_webhook=True)
    await client.start()
    await client.run(webhook_url="https://your-domain.com", path="/bot")
    await client.stop()

asyncio.run(main())
```

### ۳. ارسال و دانلود فایل

```python
async def main():
    client = BotClient("YOUR_BOT_TOKEN")
    await client.start()
    msg = await client.send_file("chat123", file="image.png", type="Image", text="Sent!")
    await client.download_file(msg.file_id, save_as="downloaded.png")
    await client.stop()

asyncio.run(main())
```

---

## سوالات متداول (FAQ)

**س: چرا آپدیت‌ها پردازش نمی‌شوند؟**\
ج: چک کنید `first_get_updates` یا `has_time_passed`. لاگ DEBUG را فعال کنید.

**س: چگونه فیلتر سفارشی بنویسم؟**\
ج: کلاس با متد `async def check(self, update) -> bool` بسازید.

**س: Webhook کار نمی‌کند؟**\
ج: URL عمومی با HTTPS و ثبت موفق `update_bot_endpoints` را چک کنید.

**س: آیا آپلود chunked پشتیبانی می‌شود؟**\
ج: خیر؛ از `aiohttp.FormData` ساده استفاده می‌شود.

## پیوست: مثال‌های پیشرفته

### بات با هندلر Sync و فیلتر سفارشی

```python
from rubpy import BotClient
from rubpy.bot import filters
from rubpy.bot.models import Update

class CustomFilter(filters.Filter):
    def check(self, update: Update) -> bool:
        return bool(update.new_message and "hello" in update.new_message.text.lower())

app = BotClient("YOUR_BOT_TOKEN")

@app.on_update(CustomFilter, filters.text)
def handle_hello(client: BotClient, update: Update):
    update.reply("Hello detected!")

app.run()
```
