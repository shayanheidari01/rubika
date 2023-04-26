# مدیریت به روز رسانی ها
___
## تعریف به روزرسانی
به‌روزرسانی‌ها رویدادهایی هستند که در اکانت روبیکا شما اتفاق می‌افتند (پیام‌های دریافتی، عضویت اعضای جدید، فشار دادن دکمه‌های ربات و غیره) که به منظور اطلاع شما از وضعیت جدیدی که تغییر کرده است، می‌باشد. این به روز رسانی ها با ثبت یک یا چند عملکرد برگشت به تماس در برنامه شما با استفاده از Handlers انجام می شود.

هر کنترل کننده با یک رویداد خاص سروکار دارد و به محض اینکه یک به روز رسانی منطبق از روبیکا دریافت شود، تابع callback ثبت شده شما توسط فریمورک فراخوانی می شود و بدنه آن اجرا می شود.

## استفاده از دکوراتورها
زیباترین راه برای ثبت یک کنترل کننده پیام، استفاده از دکوراتور  @client.on است.
```python
from rubpy import Client, handlers, Message
import asyncio

async def main():
    async with Client(session='MyAccount') as client:
        @client.on(handlers.MessageUpdates())
        async def updates(message: Message):
            if message.raw_text != None and message.raw_text == 'سلام':
                await message.reply('`hello` __from__ **rubpy**')
        await client.run_until_disconnected()

asyncio.run(main())
```
در کد بالا از کلاس handlers کنترل کننده MessageUpdates را فراخوانی کردیم و جدیدترین پیام ها را دریافت میکنیم، در کد بالا به محض اینکه کسی به شما "سلام" کند ربات به او پاسخ میدهد.
## کلاس handlers
کلاس handlers شامل 5 کلاس است(ممکن است افزایش یابد) که عبارتند از: `ChatUpdates`، `MessageUpdates`، `ShowActivities`، `ShowNotifications`، `RemoveNotifications`

ورودی این کلاس ها models هستند، اگر __any برابر true باشد، عملگر OR بین فیلترها قرار می گیرد، در غیر این صورت روی AND قرار میگیرد.
#### از کلاس models میتوانید به عنوان یک فیلتر در کلاس handlers استفاده کنید:
```python
from rubpy import models

@client.on(handlers.MessageUpdates(models.is_group))
```
* در مثال بالا ما از `models.is_group` برای دریافت آپدیت های گروه ها استفاده کرده ایم، این یعنی اگر به روزرسانی جدیدی دریافت کنیم، فقط به روزرسانی های گروه را برای ما دریافت میکند.
### فیلترها می توانند تابع باشند به عنوان مثال:
```python
from rubpy import handlers

async def custom_filter(message, result):
    return message.raw_text

handlers.MessageUpdates(custom_filter)
```
## دریافت به‌روزرسانی ها (افزودن handler)
```python
async with Client(session='rubpy') as client:
    @client.on(handler)
    async def updates(message: Message):
        pass
    @client.on(handler)
    async def updates(message: Message):
        pass

# ----- OR -----

async with Client(session='rubika') as client:
    async def updates(message: Message):
        pass
    
    client.add_handler(updates, handler)
    
```
### نکات
- فیلترها می توانند توابع باشند
- بین فیلترها می توانید از عملگرهای |, &, !=, ==, >, >=, <, <= استفاده کنید
- برای استفاده از عملگرها باید فیلتر (models) فراخوانی شود
- در آینده در مورد models بیشتر صحبت خواهیم کرد

<p align="center">
    <a href="https://github.com/shayanheidari01/rubika/blob/master/docs/Error-Handling.md">
        صفحه بعدی
    </a>
  •
  <a href="https://github.com/shayanheidari01/rubika/blob/master/docs/Authorization.md">
        صفحه قبلی
    </a>
</p>
