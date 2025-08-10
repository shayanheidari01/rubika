

**مستندات Enumها در `rubpy.bot.enums`**

> این مستندات به زبان فارسی آماده شده‌اند تا تمامی `Enum`های استفاده‌شده در ماژول‌های `rubpy.bot` را شرح دهند. هدف این است که توسعه‌دهندگان به‌سرعت معنای هر مقدار، محل استفادهٔ معمول و نمونهٔ کد را پیدا کنند.

---

## فهرست

* مقدمه: چرا از `STREnum` استفاده شده؟
* نحوهٔ استفادهٔ سریع
* توضیح هر Enum و اعضای آن

  * ChatTypeEnum
  * ForwardedFromEnum
  * PaymentStatusEnum
  * PollStatusEnum
  * LiveLocationStatusEnum
  * ButtonSelectionTypeEnum
  * ButtonSelectionSearchEnum
  * ButtonSelectionGetEnum
  * ButtonCalendarTypeEnum
  * ButtonTextboxTypeKeypadEnum
  * ButtonTextboxTypeLineEnum
  * ButtonLocationTypeEnum
  * ButtonTypeEnum
  * MessageSenderEnum
  * UpdateTypeEnum
  * ChatKeypadTypeEnum
  * UpdateEndpointTypeEnum
* مثال‌های عملی و نکات پیاده‌سازی
* توصیه‌ها و بهترین شیوه‌ها

---

## مقدمه: چرا از `STREnum` استفاده شده؟

در این پروژه همهٔ enumها از پایهٔ `STREnum` که از `str` و `Enum` ارث‌بری می‌کند مشتق شده‌اند. علت:

* مطابقت مستقیم با رشته‌های برگشتی/منتقل‌شده توسط API (بدون نیاز به فراخوانی `.value`).
* قابلیت مقایسهٔ مستقیم با رشته‌ها و آسان‌تر شدن سریال‌سازی به JSON.

**نکته:** چون `STREnum` از `str` مشتق شده است، می‌توانید مقدار enum را مستقیماً با رشتهٔ مربوطه مقایسه کنید یا آن را در JSON بنویسید.

```python
from rubpy.bot.enums import ChatTypeEnum

if chat.chat_type == ChatTypeEnum.User:
    # همچنین معتبر است:
if chat.chat_type == 'User':
    pass
```

---

## نحوهٔ استفادهٔ سریع

```python
from rubpy.bot.enums import UpdateTypeEnum, ButtonTypeEnum

# دریافت نوع آپدیت
if update.type == UpdateTypeEnum.NewMessage:
    # پردازش پیام جدید
    pass

# بررسی نوع دکمه
if some_button.type == ButtonTypeEnum.Payment:
    # پردازش پرداخت
    pass
```

---

## شرح Enumها

### `ChatTypeEnum`

نمایانگر نوع چت یا مخاطب.

* `User` — چت تک‌نفره با یک کاربر
* `Bot` — چت با یک بات
* `Group` — گروه
* `Channel` — کانال

**محل استفاده:** فیلد `chat_type` در مدل `Chat`.

---

### `ForwardedFromEnum`

منبع فوروارد پیام.

* `User` — از کاربر فوروارد شده
* `Channel` — از یک کانال فوروارد شده
* `Bot` — از یک بات فوروارد شده

---

### `PaymentStatusEnum`

وضعیت پرداخت‌های درون‌رابطه‌ای.

* `Paid` — پرداخت انجام شده
* `NotPaid` — پرداخت انجام نشده

**محل استفاده:** مدل `PaymentStatus`.

---

### `PollStatusEnum`

وضعیت نظرسنجی‌ها.

* `Open` — نظرسنجی فعال است
* `Closed` — نظرسنجی بسته شده

---

### `LiveLocationStatusEnum`

وضعیت موقعیت زنده (Live Location).

* `Stopped` — موقعیت زنده متوقف شده
* `Live` — موقعیت در حالِ اشتراک‌گذاری است

---

### `ButtonSelectionTypeEnum`

نوع نمایش آیتم‌های انتخاب در دکمه‌ها.

* `TextOnly` — فقط متن
* `TextImgThu` — متن + تصویر بندانگشتی
* `TextImgBig` — متن + تصویر بزرگ

---

### `ButtonSelectionSearchEnum`

چگونگی جستجو در آیتم‌های انتخابی.

* `NONE` (مقدار رشته‌ای "None") — غیرفعال
* `Local` — جستجوی محلی
* `Api` — جستجوی مبتنی بر API

---

### `ButtonSelectionGetEnum`

نحوهٔ واکشی آیتم انتخاب (local یا api).

* `Local`
* `Api`

---

### `ButtonCalendarTypeEnum`

نوع تقویم برای ورودی تاریخ در دکمه‌ها.

* `DatePersian` — تاریخ شمسی
* `DateGregorian` — تاریخ میلادی

---

### `ButtonTextboxTypeKeypadEnum`

نوع دادهٔ ورودی از صفحه‌کلید برای textbox.

* `String` — رشته
* `Number` — عدد

---

### `ButtonTextboxTypeLineEnum`

حالت خطی textbox.

* `SingleLine` — تک‌خطی
* `MultiLine` — چندخطی

---

### `ButtonLocationTypeEnum`

نحوهٔ نمایش/انتخاب موقعیت در دکمهٔ موقعیت.

* `Picker` — حالت انتخابگر
* `View` — حالت فقط نمایش

---

### `ButtonTypeEnum`

فهرست نوع‌های کامل دکمه که توصیفگر عملیاتی است که دکمه انجام می‌دهد.

مقادیر اصلی:

* `Simple`, `Selection`, `Calendar`, `NumberPicker`, `StringPicker`, `Location`, `Payment`,
  `CameraImage`, `CameraVideo`, `GalleryImage`, `GalleryVideo`, `File`, `Audio`,
  `RecordAudio`, `MyPhoneNumber`, `MyLocation`, `Textbox`, `Link`,
  `AskMyPhoneNumber`, `AskLocation`, `Barcode`

**توضیح کوتاه:**

* `Payment` — دکمه مربوط به شروع فرایند پرداخت
* `CameraImage` / `GalleryImage` — انتظار فایل تصویری از دوربین یا گالری
* `Textbox` — باز کردن یک فیلد متنی برای کاربر

---

### `MessageSenderEnum`

فرستندهٔ پیام: `User` یا `Bot`.

---

### `UpdateTypeEnum`

نوعِ آپدیت ارسالی توسط سرور به بات.

* `UpdatedMessage` — پیام ویرایش شده
* `NewMessage` — پیام جدید
* `RemovedMessage` — پیام حذف شده
* `StartedBot` — کاربر بات را استارت کرده
* `StoppedBot` — کاربر بات را متوقف کرده
* `UpdatedPayment` — تغییر وضعیت پرداخت

**محل استفاده:** فیلد `type` در مدل `Update`.

---

### `ChatKeypadTypeEnum`

نوع به‌روزرسانی کیپد (کیبورد) در چت.

* `NONE` (`"None"`) — هیچ تغییری
* `New` — ارسال یک کیپد جدید
* `Remove` — حذف کیپد

---

### `UpdateEndpointTypeEnum`

نوع ورودی endpoint در ارتباطات داخلی/وبهوک.

* `ReceiveUpdate` — دریافت آپدیت عادی
* `ReceiveInlineMessage` — دریافت پیام اینلاین
* `ReceiveQuery` — دریافت یک query
* `GetSelectionItem` — واکشی آیتم انتخابی
* `SearchSelectionItems` — جستجوی آیتم‌های انتخابی

---

## مثال‌های عملی و نکات پیاده‌سازی

* مقایسهٔ مستقیم با رشته:

```python
from rubpy.bot.enums import ChatTypeEnum

if chat.chat_type == ChatTypeEnum.Group:
    print('این یک گروه است')

# یا معادل:
if chat.chat_type == 'Group':
    print('این یک گروه است')
```

* سریال‌سازی به JSON:

```python
import json
from rubpy.bot.enums import UpdateTypeEnum

payload = {'type': UpdateTypeEnum.NewMessage}
# json.dumps به‌صورت خودکار مقدار enum را به رشته تبدیل می‌کند
print(json.dumps(payload))  # {"type": "NewMessage"}
```

* دریافت از API و تبدیل به enum (اگر لازم است بررسی کنید):

```python
from rubpy.bot.enums import UpdateTypeEnum

raw = 'UpdatedMessage'
try:
    t = UpdateTypeEnum(raw)
except ValueError:
    # مقدار نامعتبر از سرور دریافت شد — مدیریت خطا
    t = None
```

---

## توصیه‌ها و بهترین شیوه‌ها

1. همیشه فرض کنید مقادیر ورودی از سرور ممکن است تغییر کنند یا عضو جدید اضافه شود — هنگام تبدیل رشته‌ها به Enum از مدیریت خطا استفاده کنید.
2. از توانایی مقایسهٔ مستقیم enumها با رشته‌ها بهره ببرید تا خوانایی کد بهتر شود.
3. برای مستندسازی API و تست‌ها، مقادیر enum را به‌صورت رشته‌ای در نمونه‌داده‌ها استفاده کنید تا شباهت با payload واقعی حفظ شود.
4. هنگام تعریف کیپد/دکمه‌ها، از `ButtonTypeEnum` برای تصمیم‌گیری دربارهٔ پردازش هر دکمه استفاده کنید (مثلاً اگر نوع `Payment` است، مسیر پرداخت را اجرا کن).

---
