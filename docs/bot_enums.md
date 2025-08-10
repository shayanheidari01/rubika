# مستندات rubpy.bot.enums

این مستندات به توضیح کلاس‌ها و ثابت‌های تعریف شده در فایل `enums.py` می‌پردازد که برای مدیریت انواع داده‌های ثابت (Enumerations) در پروژه استفاده می‌شوند. این فایل شامل مجموعه‌ای از کلاس‌های مبتنی بر `Enum` است که برای دسته‌بندی و مدیریت انواع مختلف داده‌ها مانند نوع چت، نوع دکمه، وضعیت پرداخت و غیره به کار می‌روند.

## ساختار و توضیحات

### کلاس پایه: STREnum
کلاس `STREnum` به عنوان یک کلاس پایه برای تمام ثابت‌های رشته‌ای (string-based enums) تعریف شده است. این کلاس از `str` و `Enum` ارث‌بری می‌کند تا مقادیر ثابت به صورت رشته‌ای و قابل مدیریت باشند.

```python
from enum import Enum

class STREnum(str, Enum):
    pass
```

### ثابت‌های تعریف‌شده

#### 1. ChatTypeEnum
این ثابت نوع چت را مشخص می‌کند:
- `USER`: چت با یک کاربر
- `BOT`: چت با یک ربات
- `GROUP`: چت گروهی
- `CHANNEL`: چت در کانال

#### 2. ForwardedFromEnum
مشخص‌کننده منبع پیام فوروارد شده:
- `USER`: پیام از یک کاربر
- `CHANNEL`: پیام از یک کانال
- `BOT`: پیام از یک ربات

#### 3. PaymentStatusEnum
وضعیت پرداخت را مشخص می‌کند:
- `Paid`: پرداخت شده
- `NotPaid`: پرداخت نشده

#### 4. PollStatusEnum
وضعیت نظرسنجی:
- `OPEN`: نظرسنجی باز
- `CLOSED`: نظرسنجی بسته

#### 5. LiveLocationStatusEnum
وضعیت موقعیت مکانی زنده:
- `STOPPED`: موقعیت مکانی متوقف شده
- `LIVE`: موقعیت مکانی فعال

#### 6. ButtonSelectionTypeEnum
نوع انتخاب دکمه:
- `TextOnly`: فقط متن
- `TextImgThu`: متن و تصویر کوچک
- `TextImgBig`: متن و تصویر بزرگ

#### 7. ButtonSelectionSearchEnum
نوع جستجوی دکمه انتخاب:
- `NONE`: بدون جستجو
- `Local`: جستجوی محلی
- `Api`: جستجو از طریق API

#### 8. ButtonSelectionGetEnum
روش دریافت دکمه انتخاب:
- `Local`: دریافت محلی
- `Api`: دریافت از API

#### 9. ButtonCalendarTypeEnum
نوع تقویم دکمه:
- `DatePersian`: تقویم پارسی
- `DateGregorian`: تقویم میلادی

#### 10. ButtonTextboxTypeKeypadEnum
نوع صفحه‌کلید برای جعبه متن:
- `STRING`: رشته‌ای
- `NUMBER`: عددی

#### 11. ButtonTextboxTypeLineEnum
نوع خط جعبه متن:
- `SingleLine`: تک‌خطی
- `MultiLine`: چندخطی

#### 12. ButtonLocationTypeEnum
نوع دکمه موقعیت:
- `PICKER`: انتخاب‌گر موقعیت
- `VIEW`: نمایش موقعیت

#### 13. ButtonTypeEnum
انواع دکمه‌های موجود:
- `SIMPLE`: دکمه ساده
- `SELECTION`: دکمه انتخاب
- `CALENDAR`: دکمه تقویم
- `NumberPicker`: انتخاب‌گر عدد
- `StringPicker`: انتخاب‌گر رشته
- `LOCATION`: دکمه موقعیت
- `PAYMENT`: دکمه پرداخت
- `CameraImage`: تصویر دوربین
- `CameraVideo`: ویدئو دوربین
- `GalleryImage`: تصویر گالری
- `GalleryVideo`: ویدئو گالری
- `FILE`: فایل
- `AUDIO`: صدا
- `RecordAudio`: ضبط صدا
- `MyPhoneNumber`: شماره تلفن من
- `MyLocation`: موقعیت من
- `Textbox`: جعبه متن
- `LINK`: لینک
- `AskMyPhoneNumber`: درخواست شماره تلفن
- `AskLocation`: درخواست موقعیت
- `BARCODE`: بارکد

#### 14. MessageSenderEnum
فرستنده پیام:
- `USER`: کاربر
- `BOT`: ربات

#### 15. UpdateTypeEnum
نوع به‌روزرسانی:
- `UpdatedMessage`: پیام به‌روزرسانی شده
- `NewMessage`: پیام جدید
- `RemovedMessage`: پیام حذف شده
- `StartedBot`: ربات شروع شده
- `StoppedBot`: ربات متوقف شده
- `UpdatedPayment`: پرداخت به‌روزرسانی شده

#### 16. ChatKeypadTypeEnum
نوع صفحه‌کلید چت:
- `NONE`: بدون صفحه‌کلید
- `NEW`: صفحه‌کلید جدید
- `REMOVE`: حذف صفحه‌کلید

#### 17. UpdateEndpointTypeEnum
نوع نقطه پایانی به‌روزرسانی:
- `ReceiveUpdate`: دریافت به‌روزرسانی
- `ReceiveInlineMessage`: دریافت پیام اینلاین
- `ReceiveQuery`: دریافت پرس‌وجو
- `GetSelectionItem`: دریافت آیتم انتخاب
- `SearchSelectionItems`: جستجوی آیتم‌های انتخاب

## استفاده
برای استفاده از این ثابت‌ها، کافی است ماژول را وارد کرده و از کلاس‌های موردنظر استفاده کنید. به عنوان مثال:

```python
from enums import ChatTypeEnum, ButtonTypeEnum

# بررسی نوع چت
chat_type = ChatTypeEnum.USER
print(chat_type)  # خروجی: User

# بررسی نوع دکمه
button_type = ButtonTypeEnum.SIMPLE
print(button_type)  # خروجی: Simple
```

## نکات
- تمام ثابت‌ها به صورت رشته‌ای هستند و از `STREnum` ارث‌بری می‌کنند.
- ثابت‌ها به صورت واضح و خوانا نام‌گذاری شده‌اند تا استفاده از آن‌ها در کد ساده باشد.
- از `__all__` برای مشخص کردن کلاس‌های قابل صادر استفاده شده است تا از وارد کردن کلاس‌های غیرضروری جلوگیری شود.
