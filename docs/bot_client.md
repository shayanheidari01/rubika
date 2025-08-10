# BotClient — مستندات کامل (`bot_client.md`)

> این مستندات توضیح کامل و دقیق کلاس `BotClient` را بر اساس کد ارائه‌شده شامل شرح متدها، پارامترها، مقادیر بازگشتی، مثال‌های استفاده، مدل همزمانی و نکات آماده‌سازی و رفع خطا ارائه می‌دهد. تمام مثال‌ها به‌صورت `async` و برای اجرا در یک اسکریپت پایتون مدرن (۳.۸+) نوشته شده‌اند.

---

# فهرست مطالب

* خلاصه و هدف
* پیش‌نیازها و وارد کردن ماژول‌ها
* معماری و رفتار کلی
* ساختار داده‌ها و مدل‌های مرتبط
* نمونه‌سازی `BotClient`
* متدها (شرح کامل)

  * مدیریت جلسه و چرخه عمر (`start`, `stop`, `run`, `close`)
  * درخواست‌ها و محدودیت نرخ (`_make_request`, `_rate_limit_delay`)
  * اطلاعات حساب (`get_me`)
  * ارسال پیام‌ها (`send_message`, `send_sticker`, `send_file`, `send_poll`, `send_location`, `send_contact`)
  * آپلود/دانلود فایل (`request_send_file`, `upload_file`, `get_file`, `download_file`)
  * دریافت و پردازش آپدیت‌ها (`get_updates`, `updater`, `_parse_update`, `process_update`, `_filters_pass`, `on_update`)
  * مدیریت پیام‌ها (`forward_message`, `edit_message_text`, `edit_message_keypad`, `delete_message`, `set_commands`, `edit_chat_keypad`, `update_bot_endpoints`)
  * وبهوک (`handle_webhook`)
  * کمکی‌ها (`_extract_message_id`, `has_time_passed`, `get_extension`)
* ثبت هندلرها و فیلترها
* الگوی همزمانی و نکات ایمنی رشته/تسک
* نکات و بهترین شیوه‌ها
* خطاها و شیوه‌ی دیباگ
* مثال‌های کامل
* سوالات متداول (FAQ)
* تغییرات پیشنهادی و محدودیت‌ها
* پیوست: مثال‌های کدنویسی

---

# خلاصه و هدف

`BotClient` یک کلاینت برای تعامل با Bot API (در این کد: `https://botapi.rubika.ir/v3/<token>/`) است که:

* هم از مدل polling (پرس‌وجو دوره‌ای با `getUpdates`) پشتیبانی می‌کند و هم از webhook.
* دارای سیستم ثبت هندلر بر اساس فیلترها (`Filter`) است.
* عملیات ارسال پیام، فایل، موقعیت، مخاطب و نظرسنجی را پشتیبانی می‌کند.
* آپلود / دانلود فایل با متدهای کمکی دارد.
* محدودیت نرخ (rate limiting) داخلی دارد که به کمک `rate_limit` کنترل می‌شود.
* متدهای کلیدی به‌صورت `async` پیاده‌سازی شده‌اند؛ اما هنگام اجرای هندلرهای هم‌زمان از `asyncio.create_task` یا `threading.Thread` استفاده می‌شود تا هندلرهای sync هم قابل اجرا باشند.

---

# پیش‌نیازها و وارد کردن ماژول‌ها

```python
import asyncio
import dataclasses
from pathlib import Path
from typing import List, Optional, Union, Callable, Dict, Tuple, Any
import aiohttp
from aiohttp import web
# همچنین انواع/مدل‌های پروژه:
from rubpy.bot.enums import ChatKeypadTypeEnum, UpdateTypeEnum
from rubpy.bot.filters import Filter
from rubpy.bot.models import Keypad, InlineMessage, Update, Message
from rubpy.bot.models.bot import Bot
from rubpy.bot.models.chat import Chat
from rubpy.bot.models.message import MessageId
```

---

# معماری و رفتار کلی

* `BotClient` هنگام ساخت، `token` را دریافت و `base_url` را تنظیم می‌کند.
* ارتباط با سرور از طریق متد خصوصی `_make_request` انجام می‌شود که درخواست را با `POST` ارسال می‌کند و پاسخ JSON را پردازش می‌نماید.
* محدودیت نرخ به‌صورت ساده: قبل از هر درخواست `_rate_limit_delay` صبر می‌کند تا حداقل `rate_limit` ثانیه بین درخواست‌ها حفظ شود.
* آپدیت‌ها از دو مسیر گرفته می‌شوند: polling (متد `updater`) و webhook (`handle_webhook`).
* هندلرها با دکوراتور `on_update` ثبت می‌شوند؛ فیلترها هرکدام دارای متد `check` هستند که یک `await` دارد.

---

# مدل‌های کلیدی (خلاصه)

> توضیحات کاملِ کلاس‌های `Update`, `InlineMessage`, `MessageId`, `Keypad`, `Bot`, `Chat` در کد اصلی پروژه قرار دارند. اینجا خلاصه‌ای آورده شده است:

* `Update`
  نمایانگر یک به‌روزرسانی از نوع پیام جدید، به‌روزرسانی پیام یا حذف پیام. فیلدهای مهم: `type`, `chat_id`, `new_message` (پیام جدید به‌صورت `Message`), `updated_message`, `removed_message_id`, `client`.

* `InlineMessage`
  پیام‌های اینلاین که مستقیم از وبهوک یا API می‌آیند. فیلدها: `sender_id`, `text`, `message_id`, `chat_id`, `file`, `location`, `aux_data`, `client`.

* `MessageId`
  پاسخ تایید ارسال پیام که شامل `chat_id`, `message_id`, (و در send\_file ممکن است `file_id`) و غیره است.

* `Keypad`
  مدل نمایانگر کلید‌های چت (keyboard / inline keyboard)؛ قبل از ارسال باید به دیکشنری تبدیل شود (`dataclasses.asdict(keypad)`).

* `ChatKeypadTypeEnum`, `UpdateTypeEnum`
  Enumهایی که نوع keypad یا نوع آپدیت را مشخص می‌کنند.

---

# نمونه‌سازی `BotClient`

```python
from rubpy.bot.client import BotClient  # مسیر فرضی با توجه به پروژه شما
client = BotClient(token="YOUR_BOT_TOKEN", rate_limit=0.5)
```

`rate_limit` (پیش‌فرض 0.5) یعنی حداقل ۰.۵ ثانیه بین هر درخواست.

---

# شرح متدها

> برای هر متد: امضا، پارامترها، خروجی، توضیح مختصر، مثال.

---

## `async def start(self) -> None`

* کار: ایجاد `aiohttp.ClientSession()` در صورت بسته بودن یا None و ست کردن `self.running = True`.
* بازگشت: `None`
* مثال:

```python
await client.start()
```

---

## `async def stop(self) -> None`

* کار: بستن جلسه (session) در صورت باز بودن و ست کردن `self.running = False`.
* بازگشت: `None`

---

## `async def _rate_limit_delay(self) -> None`

* کار: تنظیم فاصله زمانی بین درخواست‌ها براساس `self.rate_limit`.
* داخلی: قبل از هر `_make_request` فراخوانی شود.

---

## `async def _make_request(self, method: str, data: Dict) -> Dict`

* پارامترها:

  * `method`: نام متد API (مثل `'sendMessage'`).
  * `data`: دیکشنری payload.
* رفتار:

  * فراخوانی `_rate_limit_delay`
  * `POST` به `self.base_url + method` با JSON payload
  * چک کردن `response.status` و `result['status']=='OK'`
* بازگشت:

  * در حالت موفق: `result['data']` (دیکشنری)
  * در خطا: لاگ شده و یک دیکشنری با `{"status": "ERROR", "error": str(e)}` برمی‌گرداند.
* هشدارها:

  * این متد ممکن است `aiohttp.ClientResponseError` یا دیگر استثناها را لاگ کند.
* نکته:

  * فراخوانی‌کننده باید وجود کلیدهای مورد نیاز را بررسی کند.

---

## `async def get_me(self) -> Bot`

* کار: فراخوانی `getMe` و ساخت مدل `Bot`.
* بازگشت: نمونه `Bot`.

---

## `async def send_message(self, chat_id: str, text: str, chat_keypad: Optional[Keypad]=None, inline_keypad: Optional[Keypad]=None, disable_notification: bool=False, reply_to_message_id: Optional[str]=None, chat_keypad_type: ChatKeypadTypeEnum=ChatKeypadTypeEnum.NONE) -> MessageId`

* عمل: ارسال پیام متنی با گزینه‌های کیپد و پاسخ.
* بازگشت: `MessageId` (با فیلد `chat_id` و `client` اضافه شده).
* نکته: `chat_keypad` و `inline_keypad` باید به `dataclasses.asdict()` تبدیل شوند.

---

## `async def send_sticker(self, chat_id: str, sticker_id: str, ...) -> MessageId`

* مشابه `send_message` اما با پارامتر `sticker_id`.

---

## `async def send_file(self, chat_id: str, file: Optional[Union[str, Path]]=None, file_id: Optional[str]=None, text: Optional[str]=None, file_name: Optional[str]=None, type: Literal['File','Image','Voice','Music','Gif','Video']='File', chat_keypad: Optional[Keypad]=None, inline_keypad: Optional[Keypad]=None, disable_notification: bool=False, reply_to_message_id: Optional[str]=None, chat_keypad_type: ChatKeypadTypeEnum=ChatKeypadTypeEnum.NONE) -> MessageId`

* رفتار:

  * اگر `file` داده شده: ابتدا `request_send_file(type)` برای گرفتن `upload_url`، سپس `upload_file(upload_url, file_name, file)` برای گرفتن `file_id`.
  * سپس `sendFile` فراخوانی می‌شود با `file_id`.
* بازگشت: `MessageId` شامل `file_id`.
* نکات ایمنی:

  * `upload_file` فعلاً فایل را با `open(file_path, 'rb')` باز می‌کند بدون `with` — بهتر است بازنویسی شود تا فایل بسته شود یا از stream استفاده شود.
  * `upload_file` یک `aiohttp.ClientSession()` محلی باز می‌کند و `ssl=False` ارسال می‌کند — در محیط‌های امن این مورد را بررسی کنید.

---

## `async def request_send_file(self, type: Literal[...]) -> str`

* کار: گرفتن `upload_url` از API برای انواع مشخص.
* بازگشت: `upload_url` (رشته).
* خطا: اگر `type` نامعتبر باشد `ValueError` برمی‌گرداند.

---

## `async def upload_file(self, url: str, file_name: str, file_path: str) -> str`

* کار: ارسال multipart/form-data به `url` با فیلد `file`.
* بازگشت: `file_id` (رشته) طبق ساختار پاسخ API (`data['file_id']`).
* هشدار:

  * فایل باز با `open(file_path, 'rb')` و سپس به `aiohttp.FormData()` اضافه می‌شود — در نسخه فعلی هنگام خطا ممکن است handle فایل باز بماند؛ بهتر است با `with open(...) as f:` و اضافه‌سازی فایل به فرم استفاده شود.
  * `ssl=False` در `session.post` تعیین شده — ممکن است امنیت را کاهش دهد.

---

## `async def get_file(self, file_id: str) -> str`

* کار: فراخوانی `getFile` و بازگردانی `download_url`.
* بازگشت: `download_url`

---

## `async def download_file(self, file_id: str, save_as: Optional[str]=None, progress: Optional[Callable[[int,int],None]]=None, chunk_size: int=65536, as_bytes: bool=False) -> Union[str, bytes, None]`

* کار:

  * گرفتن `download_url`، ارسال POST به `download_url`، خواندن جریان پاسخ و ذخیره یا برگرداندن بایت‌ها.
* پارامترها:

  * `save_as`: مسیر فایل برای ذخیره (اگر `as_bytes=False`).
  * `progress`: تابع callback که `(downloaded, total_size)` می‌گیرد.
  * `as_bytes`: اگر `True` محتوای فایل را به‌صورت `bytes` برمی‌گرداند.
* بازگشت:

  * مسیر ذخیره‌شده یا `bytes` یا `None` در صورت خطا.
* نکات:

  * header `Content-Type` خوانده می‌شود و از `get_extension` برای تعیین پسوند استفاده می‌شود.
  * اگر `Content-Length` موجود نباشد، `total_size=0`.

---

## `async def send_poll(self, chat_id: str, question: str, options: List[str]) -> MessageId`

* کار: ارسال نظرسنجی.
* بازگشت: `MessageId`

---

## `async def send_location(self, chat_id: str, latitude: Union[str,float], longitude: Union[str,float], ...) -> MessageId`

* پارامترها: `latitude`, `longitude` (می‌توان string یا float فرستاد) و پارامترهای اختیاری مشابه `send_message`.
* بازگشت: `MessageId`

---

## `async def send_contact(self, chat_id: str, first_name: str, last_name: str, phone_number: str, ...) -> MessageId`

* ارسال اطلاعات مخاطب به چت.

---

## `async def get_updates(self, limit: int = 100, offset_id: str = "") -> List[Union[Update, InlineMessage]]`

* کار: دریافت بلافاصله آپدیت‌ها (یک فراخوانی سریع).
* پارامتر: `limit`, `offset_id`
* بازگشت: لیست از `Update` یا `InlineMessage` (در این متد فقط فیلتر ساده‌ای انجام می‌شود؛ تبدیل پایه‌ای به `Update` انجام می‌شود).

---

## `async def updater(self, limit: int = 100, offset_id: str = "") -> List[Union[Update, InlineMessage]]`

* کار: مشابه `get_updates` اما با مدیریت `self.next_offset_id` و استفاده از `_parse_update`.
* رفتار:

  * پس از اولین بار (زمانی که `self.first_get_updates` True است) یک لیست خالی بازمی‌گرداند تا پیام‌های قدیمی پردازش نشوند.
  * برای هر آپدیت `_parse_update` فراخوانی می‌شود.
  * اگر زمان پیام بیشتر از ۵ ثانیه گذشته باشد (با `has_time_passed`) آن را نادیده می‌گیرد.
* بازگشت: لیست از اشیاء `Update` یا `InlineMessage`.

---

## `def on_update(self, *filters: Filter) -> Callable`

* کار: دکوراتوری برای ثبت هندلرها.
* مثال:

```python
@client.on_update(MyFilter(), AnotherFilter())
async def handler(client: BotClient, update: Update):
    ...
```

* توضیح: برای هر handler یک `filter_key` یونیک ساخته می‌شود و در `self.handlers` ثبت می‌شود. `filters` می‌تواند کلاس فیلتر یا نمونه باشد؛ اگر کلاس فرستاده شود در زمان بررسی نمونه‌سازی می‌شود.

---

## `def _parse_update(self, item: Dict) -> Optional[Union[Update, InlineMessage]]`

* کار: تبدیل دیکشنری دریافتی از API به اشیاء `Update` یا `InlineMessage`.
* پشتیبانی:

  * `UpdateTypeEnum.REMOVED_MESSAGE` → ساخت یک `Update` با `removed_message_id`
  * `UpdateTypeEnum.NEW_MESSAGE`, `UpdateTypeEnum.UPDATED_MESSAGE` → تبدیل `msg_data` به `Message` و سپس `Update`
  * `"InlineMessage"` → ساخت `InlineMessage`
* خطاها: اگر پارس پیام ناموفق باشد، لاگ و `None` برمی‌گردد.

---

## `async def process_update(self, update: Union[Update, InlineMessage]) -> None`

* کار: مدیریت اجرای handlerهای مرتبط با یک آپدیت:

  * استخراج `message_id` با `_extract_message_id` و جلوگیری از پردازش تکراری (با `self.processed_messages`)
  * پیمایش `self.handlers` و برای هر handler بررسی فیلترها با `_filters_pass`
  * اجرای handler: اگر async باشد از `asyncio.create_task` استفاده می‌شود؛ اگر sync باشد در یک `threading.Thread` اجرا می‌شود.
* نکته:

  * اگر هیچ handlerای منطبق نبود، لاگ WARNING می‌دهد.

---

## `def _extract_message_id(self, update: Union[Update, InlineMessage]) -> Optional[str]`

* بازگشت `message_id` مناسب (برای جلوگیری از پردازش تکراری).

---

## `async def _filters_pass(self, update: Union[Update, InlineMessage], filters: Tuple[Filter, ...]) -> bool`

* کار: اجرای متد `check` هر فیلتر (با `await`) و بازگرداندن `True` تنها اگر همه فیلترها پاس شوند.
* نکته: اگر فیلتر به‌صورت کلاس ارسال شده باشد، نمونه‌سازی انجام می‌شود.

---

## وبهوک: `async def handle_webhook(self, request: web.Request) -> web.Response`

* استفاده: برای اتصال مسیر webhook در `aiohttp` app.
* ورودی: `request` (منتظر JSON)
* کار:

  * بررسی وجود `inline_message` یا `update` در payload و تبدیل به اشیاء مناسب (`InlineMessage` یا `Update`)
  * اجرای `asyncio.create_task(self.process_update(update))` برای هر update
  * بازگرداندن json `{"status": "OK"}` در حالت موفق
* خطاها:

  * در صورت JSON نامعتبر، کد وضعیت ۴۰۰ و پیام خطا بازگردانده می‌شود.
  * در خطاهای دیگر کد وضعیت ۵۰۰ بازگردانده می‌شود.

---

## `async def run(self, webhook_url: Optional[str] = None, path: Optional[str] = '/webhook', host: str = "0.0.0.0", port: int = 8080)`

* دو حالت:

  * اگر `webhook_url` داده شود: `use_webhook=True`، یک `aiohttp` server راه‌اندازی شده و مسیرها ثبت می‌شوند. سپس `update_bot_endpoints` برای ثبت endpoint در API فراخوانی می‌شود. در حلقه `while self.running` سرور نگهداری می‌شود.
  * اگر `webhook_url` None: وارد حلقه polling می‌شود: هر بار `updater` اجرا و `process_update`ها با `create_task` اجرا می‌شوند. در صورت خطا تاخیر ۲ ثانیه و تکرار.
* نکته: در حالت وبهوک باید `update_bot_endpoints` را چک کنید.

---

## `async def close(self)`

* کار: بستن `session` در صورت باز بودن.

---

## `async def forward_message(self, from_chat_id: str, message_id: str, to_chat_id: str, disable_notification: bool=False) -> MessageId`

* رفتار: فراخوانی `forwardMessage` و بازگردانی `MessageId`.

---

## `async def edit_message_text(self, chat_id: str, message_id: str, text: str) -> Any`

* رفتار: فراخوانی `editMessageText`. اگر پاسخ `{}` باشد، `True` باز می‌گردد (فرآیند موفق). در غیر این صورت `False`.

---

## `async def edit_message_keypad(self, chat_id: str, message_id: str, inline_keypad: Keypad) -> Any`

* مشابه `edit_message_text` اما برای تعویض inline keypad.

---

## `async def delete_message(self, chat_id: str, message_id: str) -> Any`

* کار: حذف پیام. موفقیت از طریق بررسی `result == {}` اعلام می‌شود.

---

## `async def set_commands(self, commands: List[Dict[str,str]]) -> Any`

* کار: تعیین دستورات (commands) برای بات.

---

## `async def update_bot_endpoints(self, url: str, endpoint_type: str)`

* کار: تماس با API برای بروزرسانی endpointها (وبهوک).

---

## `async def edit_chat_keypad(self, chat_id: str, keypad_type: ChatKeypadTypeEnum, keypad: Optional[Keypad]=None) -> Any`

* کار: ویرایش کیپد چت (نمایش کیبورد ثابت یا حذف آن).

---

# توابع کمکی

## `def has_time_passed(last_time, seconds: int = 5) -> bool`

* تبدیل `last_time` به `int` و مقایسه با زمان فعلی.
* اگر ورودی نامعتبر باشد `False` برمی‌گرداند.

## `def get_extension(content_type: str) -> str`

* استفاده از `mimetypes.guess_extension` برای پیدا کردن پسوند بر اساس MIME type.
* خروجی: رشته مثل `'.jpg'` یا `''` اگر ناشناخته باشد.

---

# ثبت هندلرها و فیلترها — الگوی کار

* برای ثبت یک هندلر از دکوراتور `on_update` استفاده کنید:

```python
@client.on_update(SomeFilter(), AnotherFilter())
async def my_handler(client: BotClient, update: Update):
    # پردازش آپدیت
    ...
```

* `Filter` باید متد `async def check(self, update)` داشته باشد که `True/False` برمی‌گرداند.
* اگر فیلتر به‌صورت کلاس گذارده شود، `_filters_pass` آن را نمونه‌سازی خواهد کرد.

---

# الگوی همزمانی (Concurrency)

* `process_update` برای اجرای هندلرها:

  * اگر هندلر coroutine باشد: `asyncio.create_task(handler(self, update))` — اجرای ناهمگام در loop جاری.
  * اگر هندلر تابع همگام (sync) باشد: اجرا در `threading.Thread` جداگانه تا از بلاک شدن loop جلوگیری شود.
* نکته: اجرای همزمان تعداد زیادی هندلر ممکن است منجر به استفاده زیاد از منابع شود — اگر هندلرهای سنگین دارید، از صف (queue) یا یک worker pool استفاده کنید.

---

# نکات و بهترین شیوه‌ها

1. **مدیریت session:** از `await client.start()` قبل از ارسال درخواست‌ها استفاده کنید و در خاتمه `await client.stop()` یا `await client.close()`.
2. **بستن فایل‌ها:** در `upload_file` از `with open(...)` استفاده کنید تا فایل همیشه بسته شود.
3. **SSL:** `upload_file` در نمونه از `ssl=False` استفاده می‌کند — اگر endpoint شما TLS صحیح دارد، این گزینه را حذف کنید.
4. **مدیریت خطاها:** `_make_request` خطاها را لاگ می‌کند و یک ساختار خطا برمی‌گرداند؛ کد فراخوان باید پاسخ بد را مدیریت کند.
5. **Rate limit:** اگر روی سرور با ترافیک بالا کار می‌کنید، `rate_limit` مناسب انتخاب کنید تا API را تحت فشار قرار ندهید.
6. **اولین fetch:** `updater` در اولین فراخوانی آپدیت‌ها را نادیده می‌گیرد (`self.first_get_updates`) تا پیام‌های تاریخی پردازش نشوند.
7. **پردازش پیام‌های قدیمی:** شرط `has_time_passed(..., 5)` در `updater` پیام‌های قدیمی را فیلتر می‌کند — این مقدار را برحسب نیاز تنظیم کنید.
8. **پایداری در polling:** حلقه polling در `run` خطاها را گرفته و پس از ۲ ثانیه تلاش مجدد می‌کند.

---

# دیباگ و لاگ‌گیری

* `logger` در سراسر کلاس استفاده شده است (`logger.info`, `logger.debug`, `logger.error`, `logger.exception`).
* برای فعال‌سازی لاگ بیشتر در بالای برنامه:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

* از لاگ‌های `API response` و `Failed to parse message` استفاده کنید تا مشکلات مربوط به قالب پاسخ API یا داده‌ها را پی بگیرید.

---

# مثال‌های کامل

## مثال ۱ — راه‌اندازی و polling ساده

```python
import asyncio
from rubpy.bot.client import BotClient

async def main():
    client = BotClient("TOKEN_HERE", rate_limit=0.4)
    await client.start()

    @client.on_update()
    async def echo(client, update):
        if update.new_message:
            chat_id = update.chat_id
            text = update.new_message.text or "..."
            await client.send_message(chat_id, f"Echo: {text}")

    await client.run()  # حالت پیش‌فرض polling

asyncio.run(main())
```

## مثال ۲ — وبهوک (aiohttp)

```python
import asyncio
from rubpy.bot.client import BotClient

async def main():
    client = BotClient("TOKEN_HERE")
    await client.run(webhook_url="https://example.com", path="/bot/webhook", host="0.0.0.0", port=8080)

# توجه: در این حالت run سرور aiohttp را مدیریت می‌کند.
```

## مثال ۳ — ارسال فایل (local upload)

```python
await client.start()
msg = await client.send_file(chat_id="12345", file="/path/to/file.png", type="Image", text="Here you go")
print("sent file id:", msg.message_id, msg.file_id)
await client.stop()
```

## مثال ۴ — دانلود فایل با پیشرفت

```python
def progress(downloaded, total):
    print(f"{downloaded}/{total} bytes")

data = await client.download_file(file_id="abc123", save_as="out.png", progress=progress)
print("Saved file to", data)
```

---

# سوالات متداول (FAQ)

**س: وقتی هندلری ثبت می‌کنم، چگونه فیلترها اعمال می‌شوند؟**
ج: `on_update` فیلترها را به handler مربوطه اضافه می‌کند. هنگام پردازش، `_filters_pass` هر فیلتر را (اگر کلاس فرستاده شده باشد نمونه‌سازی می‌کند) و متد `check` را `await` می‌کند.

**س: چرا بعضی پیام‌ها دوبار پردازش می‌شوند؟**
ج: `processed_messages` یک `deque` با `maxlen=10000` وجود دارد که `message_id` پردازش‌شده را ذخیره می‌کند. اگر `message_id` تولید نشود یا متفاوت باشد ممکن است تکراری پردازش شود. برای InlineMessage این بررسی غیرفعال شده است چرا که ممکن است `message_id` تکراری داشته باشد.

**س: چگونه webhook را در API ثبت کنم؟**
ج: هنگام اجرای `run` با `webhook_url`، `run` خودش متد `update_bot_endpoints` را برای endpointهای `ReceiveUpdate` و `ReceiveInlineMessage` فراخوانی می‌کند.

**س: آیا `upload_file` فایل را gzip یا chunked ارسال می‌کند؟**
ج: خیر؛ `upload_file` از `aiohttp.FormData` استفاده می‌کند؛ handling chunked یا resume پیاده نشده است.


# پیوست — مثال کامل (bot script)

```python
import asyncio
import logging
from rubpy.bot.client import BotClient

logging.basicConfig(level=logging.INFO)

async def main():
    client = BotClient("TOKEN", rate_limit=0.6)
    await client.start()

    @client.on_update()
    async def pingpong(client, update):
        if update.new_message and update.new_message.text == "/ping":
            await client.send_message(update.chat_id, "pong")

    try:
        await client.run()  # polling
    finally:
        await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
```
