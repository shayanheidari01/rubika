# مدیریت به روز رسانی ها
___
## تعریف به روزرسانی
به‌روزرسانی‌ها رویدادهایی هستند که در اکانت روبیکا شما اتفاق می‌افتند (پیام‌های دریافتی، عضویت اعضای جدید، فشار دادن دکمه‌های ربات و غیره) که به منظور اطلاع شما از وضعیت جدیدی که تغییر کرده است، می‌باشد. این به روز رسانی ها با ثبت یک یا چند عملکرد برگشت به تماس در برنامه شما با استفاده از Handlers انجام می شود.

هر کنترل کننده با یک رویداد خاص سروکار دارد و به محض اینکه یک به روز رسانی منطبق از روبیکا دریافت شود، تابع callback ثبت شده شما توسط فریمورک فراخوانی می شود و بدنه آن اجرا می شود.

## استفاده از دکوراتورها
زیباترین راه برای ثبت یک کنترل کننده پیام، استفاده از دکوراتور  @client.on است.
```python
from rubpy import Client, handlers
import asyncio

async def main():
    async with Client(session='MyAccount') as client:
        @client.on(handlers.MessageUpdates())
        async def updates(update):
            if update.raw_text != None and update.raw_text == 'سلام':
                await update.reply('`hello` __from__ **rubpy**')
        await client.run_until_disconnected()

asyncio.run(main())
```
در کد بالا از کلاس handlers کنترل کننده MessageUpdates را فراخوانی کردیم و جدیدترین پیام ها را دریافت میکنیم، در کد بالا به محض اینکه کسی به شما "سلام" کند ربات به او پاسخ میدهد.
## کلاس handlers
کلاس handlers شامل 5 کلاس است(ممکن است افزایش یابد) که عبارتند از: `ChatUpdates`، `MessageUpdates`، `ShowActivities`، `ShowNotifications`، `RemoveNotifications`
ورودی این کلاس ها models هستند، اگر __any برابر true باشد، عملگر OR بین فیلترها قرار می گیرد، در غیر این صورت روی AND قرار میگیرد.
<p align="center">
    <a href="https://github.com/shayanheidari01/rubika/blob/master/docs/Error-Handling.md">
        صفحه بعدی
    </a>
  •
  <a href="https://github.com/shayanheidari01/rubika/blob/master/docs/Authorization.md">
        صفحه قبلی
    </a>
</p>
