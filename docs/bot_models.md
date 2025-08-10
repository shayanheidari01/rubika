

**مستندات مدل‌های `rubpy.bot.models`**

> این فایل مستندات به زبان فارسی برای قرارگیری در گیت‌هاب تهیه شده و تمام کلاس‌ها و ساختارهای دیتاکلاسی که در فایل مدل‌ها (models) تعریف شده‌اند را شرح می‌دهد. هدف: مرجعی خوانا برای توسعه‌دهندگان که می‌خواهند با مدل‌های داخلی کتابخانه `rubpy` کار کنند.

---

## فهرست مطالب

* معرفی کلی
* نحوه‌ی استفادهٔ سریع (Quick Start)
* شرح تک‌تک کلاس‌ها و فیلدها

  * File
  * Chat
  * ForwardedFrom
  * PaymentStatus
  * MessageTextUpdate
  * Bot
  * BotCommand
  * Sticker
  * ContactMessage
  * PollStatus و Poll
  * Location و LiveLocation
  * انواع Button و Keypad
  * Message، MessageId
  * Update
  * InlineMessage
* مثال‌های کاربردی

---

## معرفی کلی

مدل‌های این ماژول (`rubpy.bot.models`) به‌صورت `dataclass` تعریف شده‌اند و هر کدام از آن‌ها از کلاس پایه‌ای `DictLike` ارث‌بری می‌کنند که رفتار تبدیل به/از دیکشنری و دسترسی شبیه دیکشنری را فراهم می‌کند. این مدل‌ها نمایانگر آبجکت‌های سطح بالا در تعامل با API ربات (پیام، دکمه‌ها، کیپدها، فایل‌ها و ... ) هستند.

تمام فیلدها `Optional` هستند تا سازگاری با payloadهای ناقص یا کم‌اطلاعات سرویس فراهم شود.

---

## نحوهٔ استفادهٔ سریع (Quick Start)

```python
from rubpy.bot.models import Update, Keypad, Button, KeypadRow

# در یک هندلر وقتی که update به شما داده می‌شود:
async def on_update(update: Update):
    await update.reply('سلام!')

# ساخت یک کیپد ساده:
row = KeypadRow(buttons=[Button(id='btn1', type=None, button_text='خرید')])
keypad = Keypad(rows=[row])
# سپس ارسال پیام با کیپد:
# await client.send_message(chat_id, 'متن', chat_keypad=keypad)
```

---

## شرح کلاس‌ها

> در هر بخش: نام کلاس، فیلدها، توضیح هر فیلد و مثال کوتاه نمایش داده شده است.

### `File`

نمایش فایل (عکس، ویدئو، سند و ...).

* `file_id: Optional[str]` — شناسهٔ یکتای فایل که توسط سرور بازگردانده می‌شود.
* `file_name: Optional[str]` — نام فایل.
* `size: Optional[str]` — اندازهٔ فایل (معمولاً بر حسب بایت یا رشته‌ای که API برمی‌گرداند).

**مثال:**

```python
f = File(file_id='123abc', file_name='photo.jpg', size='34567')
```

---

### `Chat`

اطلاعات چت یا کاربر.

* `chat_id`, `chat_type` (از `ChatTypeEnum`), `user_id`, `first_name`, `last_name`, `title`, `username`.

این ساختار برای نگهداری متادیتای چت استفاده می‌شود.

---

### `ForwardedFrom`

مشخص‌کنندهٔ منبع فوروارد یک پیام.

* `type_from: ForwardedFromEnum`
* `message_id`, `from_chat_id`, `from_sender_id`

---

### `PaymentStatus`

نمایش وضعیت پرداخت.

* `payment_id: Optional[str]`
* `status: Optional[PaymentStatusEnum]`

---

### `MessageTextUpdate`

برای نگهداری تغییرات متن پیام (ویرایش‌ها).

* `message_id: Optional[str]`
* `text: Optional[str]`

---

### `Bot`

نمایش اطلاعات مربوط به ربات.

* `bot_id`, `bot_title`, `avatar: Optional[File]`, `description`, `username`, `start_message`, `share_url`.

---

### `BotCommand`

* `command: Optional[str]` — نام فرمان.
* `description: Optional[str]` — توضیح فرمان.

---

### `Sticker`

* `sticker_id`, `file: Optional[File]`, `emoji_character`.

---

### `ContactMessage`

* `phone_number`, `first_name`, `last_name` — برای پیام‌های نوع کانتکت.

---

### `PollStatus` و `Poll`

`PollStatus`:

* `state: Optional[PollStatusEnum]` — وضعیت نظرسنجی (مثلاً باز/بسته)
* `selection_index: Optional[int]` — ایندکس انتخاب شده
* `percent_vote_options: Optional[List[int]]` — درصد آرا برای هر گزینه
* `total_vote: Optional[int]` — مجموع آرا
* `show_total_votes: Optional[bool]` — نمایش مجموع آرا یا خیر

`Poll`:

* `question: Optional[str]`
* `options: Optional[List[str]]`
* `poll_status: Optional[PollStatus]`

---

### `Location` و `LiveLocation`

`Location`:

* `longitude: Optional[str]`, `latitude: Optional[str]` (رشته یا عدد به‌دلخواه API)

`LiveLocation`:

* `start_time`, `live_period: Optional[int]`, `current_location: Optional[Location]`,
  `user_id`, `status: Optional[LiveLocationStatusEnum]`, `last_update_time`

---

### آیتم‌های انتخاب (ButtonSelectionItem) و ButtonSelection

`ButtonSelectionItem`:

* `text`, `image_url`, `type: Optional[ButtonSelectionTypeEnum]`

`ButtonSelection`:

* `selection_id`, `search_type`, `get_type`, `items: Optional[List[ButtonSelectionItem]]`,
  `is_multi_selection: Optional[bool]`, `columns_count`, `title`

این‌ها برای نمایش لیست انتخاب چندتایی یا تک‌گزینه‌ای در کیپد/دکمه‌ها استفاده می‌شوند.

---

### انواع دکمه‌ها: `ButtonCalendar`, `ButtonNumberPicker`, `ButtonStringPicker`, `ButtonTextbox`, `ButtonLocation`

هدف: هر نوع ورودی تخصصی که در دکمه‌ها می‌توان قرار داد را مدل‌سازی می‌کنند.

* `ButtonCalendar`:

  * `default_value`, `type: ButtonCalendarTypeEnum`, `min_year`, `max_year`, `title`
* `ButtonNumberPicker`:

  * `min_value`, `max_value`, `default_value`, `title`
* `ButtonStringPicker`:

  * `items: List[str]`, `default_value`, `title`
* `ButtonTextbox`:

  * `type_line: ButtonTextboxTypeLineEnum`, `type_keypad: ButtonTextboxTypeKeypadEnum`,
    `place_holder`, `title`, `default_value`
* `ButtonLocation`:

  * `default_pointer_location: Location`, `default_map_location: Location`, `type: ButtonLocationTypeEnum`,
    `title`, `location_image_url`

---

### `AuxData`

حاوی اطلاعات کمکی که ممکن است همزمان با پیام ارسال شود، مانند `start_id` و `button_id`.

---

### `Button`

ساختار یک دکمهٔ کلی:

* `id: Optional[str]`
* `type: Optional[ButtonTypeEnum]`
* `button_text: Optional[str]`
* و فیلدهای اختصاصی هر نوع دکمه که در بالا توضیح داده شد (مثلاً `button_selection`, `button_calendar`, ...)

**مثال:**

```python
btn = Button(id='buy', type=ButtonTypeEnum.CALLBACK, button_text='خرید', button_textbox=None)
```

---

### `KeypadRow` و `Keypad`

* `KeypadRow` — شامل یک لیست از `Button`ها: `buttons: Optional[List[Button]]`
* `Keypad` — شامل `rows: Optional[List[KeypadRow]]` و تنظیمات نمایشی مانند `resize_keyboard: Optional[bool]` و `on_time_keyboard: Optional[bool]`.

این کلاس‌ها برای ساخت کیبوردهای خطی و اینلاین (inline keyboard) کاربرد دارند.

---

### `MessageKeypadUpdate`

* `message_id: Optional[str]`
* `inline_keypad: Optional[Keypad]`

برای به‌روزرسانی کیپد پیام‌ها استفاده می‌شود.

---

### `MessageId`

نمایش شناسهٔ پیام در ترکیب با عملیات کمکی.

* `message_id`, `new_message_id`, `file_id`, `chat_id`, `client: Optional["rubpy.BotClient"]`

**متدها:**

* `delete()` — حذف پیام (صدا به `client.delete_message`).
* `edit_text(new_text: str)` — ویرایش متن پیام (صدا به `client.edit_message_text`).

> دقت کنید: `client` باید ست شده باشد تا متدها کار کنند (معمولاً هنگام پردازش آپدیت، `client` به آبجکت‌های برگشتی اضافه می‌شود).

---

### `Message`

ساختار کامل پیام دریافتی:

* `message_id: Optional[MessageId]`
* `text: Optional[str]`
* `time: Optional[int]` (timestamp)
* `is_edited: Optional[bool]`
* `sender_type: Optional[MessageSenderEnum]`
* `sender_id: Optional[str]`
* `aux_data: Optional[AuxData]`
* `file: Optional[File]`
* `reply_to_message_id: Optional[str]`
* `forwarded_from: Optional[ForwardedFrom]`
* `forwarded_no_link: Optional[str]`
* `location: Optional[Location]`
* `sticker: Optional[Sticker]`
* `contact_message: Optional[ContactMessage]`
* `poll: Optional[Poll]`
* `live_location: Optional[LiveLocation]`

---

### `Update`

نمایانگر یک آپدیت از سمت API (پیام جدید، حذف پیام، ویرایش، وضعیت پرداخت و ...).

* فیلدها: `type: Optional[UpdateTypeEnum]`, `chat_id`, `removed_message_id`, `new_message: Optional[Message]`,
  `updated_message: Optional[Message]`, `updated_payment: Optional[PaymentStatus]`, `client: Optional["rubpy.BotClient"]`

**متدهای کاربردی:**

* `reply(...)` — ارسال پیام متنی سریع به همان چت (یا chat\_id مشخص). فراخوانی `client.send_message` با پارامترهای مناسب.
* `reply_file(...)` — ارسال فایل (اغلب برای عکس/ویدیو/صوت/موسیقی)
* `reply_photo(...), reply_video(...), reply_voice(...), reply_music(...), reply_gif(...)` — شورت‌کات برای ارسال نوع فایل مشخص
* `delete(chat_id=None, message_id=None)` — حذف پیام
* `download(file_id=None, save_as=None, progress=None, chunk_size=65536, as_bytes=False)` — دانلود فایل با صدا به `client.download_file`

> همۀ متدها `async` هستند و ابتدا بررسی می‌کنند که `self.client` ست شده باشد — در غیر این صورت `ValueError` پرتاب می‌شود.

**نکته:** هنگام استفاده از `reply`ها معمولاً `reply_to_message_id` به `self.new_message.message_id` یا `None` تنظیم می‌شود.

---

### `InlineMessage`

مانند `Message` اما برای پیام‌های اینلاین (که داخل باکس جستجو/نتایج اینلاین باز می‌شوند).
فیلدها شبیه `InlineMessage` (sender\_id, text, file, location, aux\_data, message\_id, chat\_id, client)

**متدها:**

* `reply`, `reply_file`, `reply_photo`, `reply_voice`, `reply_music`, `reply_gif`, `reply_video`, `delete` — مشابه `Update` اما عمل روی `self.client` و `self.chat_id`/`self.message_id` انجام می‌شود.

---

## مثال‌های کاربردی

### ۱) ارسال پاسخ ساده از داخل هندلر آپدیت

```python
async def on_update(update: Update):
    # به‌صورت پیش‌فرض chat_id از update گرفته می‌شود
    await update.reply('سلام! این یک پاسخ خودکار است.')
```

### ۲) ارسال پیام با یک کیپد ساده

```python
from rubpy.bot.models import Button, KeypadRow, Keypad

row = KeypadRow(buttons=[Button(id='btn1', button_text='✅ قبول'), Button(id='btn2', button_text='❌ رد')])
keypad = Keypad(rows=[row], resize_keyboard=True)
await update.reply('یک تاییدیه لازم است:', chat_keypad=keypad)
```

### ۳) دانلود فایلی که با پیام آمده

```python
# فرض: update.new_message.file.file_id موجود است
await update.download(save_as='downloads/photo.jpg')
# یا به‌صورت بایتی
content = await update.download(as_bytes=True)
```

### ۴) حذف پیام ارسال‌شده

```python
mid = await update.reply('پیام حذف‌شدنی')
# mid از نوع MessageId برگشت داده می‌شود و client را دارد
await mid.delete()
```
