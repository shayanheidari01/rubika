# مدیریت به روز رسانی ها
___
## تعریف به روزرسانی
به‌روزرسانی‌ها رویدادهایی هستند که در اکانت روبیکا شما اتفاق می‌افتند (پیام‌های دریافتی، عضویت اعضای جدید، فشار دادن دکمه‌های ربات و غیره) که به منظور اطلاع شما از وضعیت جدیدی که تغییر کرده است، می‌باشد. این به روز رسانی ها با ثبت یک یا چند عملکرد برگشت به تماس در برنامه شما با استفاده از Handlers انجام می شود.

هر کنترل کننده با یک رویداد خاص سروکار دارد و به محض اینکه یک به روز رسانی منطبق از روبیکا دریافت شود، تابع callback ثبت شده شما توسط فریمورک فراخوانی می شود و بدنه آن اجرا می شود.

## استفاده از دکوراتورها
زیباترین راه برای ثبت یک کنترل کننده پیام، استفاده از دکوراتور است.
```python
from rubpy import Client
from rubpy.types import Updates

bot = Client(name='rubpy')

@bot.on_message_updates()
async def updates(update: Updates):
    print(update)

bot.run()
```
در کد بالا از کلاس Client کنترل کننده on_message_updates را فراخوانی کردیم و جدیدترین پیام ها را دریافت میکنیم، در کد بالا به محض اینکه کسی به شما "سلام" کند ربات به او پاسخ میدهد.
## متدهای هندلر
کلاس Client شامل 5 کلاس است(ممکن است افزایش یابد) که عبارتند از: `on_chat_updates`، `on_message_updates`، `on_show_activities`، `on_show_notifications`، `on_remove_notifications`

ورودی این متدها filters هستند، اگر __any برابر true باشد، عملگر OR بین فیلترها قرار می گیرد، در غیر این صورت روی AND قرار میگیرد.
#### از filters میتوانید به عنوان یک فیلتر در متد استفاده کنید:
```python
from rubpy import filters

@bot.on_message_updates(filters.text)
```
* در مثال بالا ما از `models.text` برای دریافت آپدیت پیام های متنی استفاده کرده ایم، این یعنی اگر به روزرسانی جدیدی دریافت کنیم، فقط به روزرسانی های متنی را برای ما دریافت میکند.
### فیلترها می توانند تابع باشند به عنوان مثال:
```python
async def custom_filter(message, result):
    return message.raw_text

@bot.on_message_updates(custom_filter)
```
## دریافت به‌روزرسانی ها (افزودن handler)
```python
client.add_handler(updates, handler)
```
### نکات
- فیلترها می توانند توابع باشند
- بین فیلترها می توانید از عملگرهای |, &, !=, ==, >, >=, <, <= استفاده کنید
- برای استفاده از عملگرها باید فیلتر (models) فراخوانی شود
- در آینده در مورد filters بیشتر صحبت خواهیم کرد

<p align="center">
    <a href="https://github.com/shayanheidari01/rubika/blob/master/docs/Error-Handling.md">
        صفحه بعدی
    </a>
  •
  <a href="https://github.com/shayanheidari01/rubika/blob/master/docs/Authorization.md">
        صفحه قبلی
    </a>
</p>
