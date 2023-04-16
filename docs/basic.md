# شروع سریع
#### چند مرحله سریع تر شروع میکنیم، برای دیدن سرعت و عمکلکرد فریمورک روبیکا پای


## سرعت باورنکردنی روبیکا پای

1. کتابخانه را با دستور ```pip install -U  rubpy``` نصب کنید
2. ویرایشگر کد خود را باز کنید و تیکه کد زیر را در آن وارد نمایید
```python
from rubpy import Client, handlers
import asyncio

async def main():
    async with Client(session='MyAccount') as client:
        @client.on(handlers.MessageUpdates())
        async def updates(update):
            await update.reply('`hello` __from__ **rubpy**')
        await client.run_until_disconnected()

asyncio.run(main())
```
3. کلمه MyAccount نام نشست ایجاد شده از حساب کاربری شما است، میتوانید تغییر دهید.
4. فایل را به عنوان ```hello.py``` ذخیره کنید.
5. فایل پایتونی را با دستور ```python3 hello.py``` اجرا کنید.
6. اگر پیام جدیدی دریافت کنید، خواهید دید که روبیکا پای به آن پاسخ داده است.

# از API لذت ببرید
###### این فقط یک مرور سریع بود. در چند صفحه بعدی مقدمه، نگاه بسیار عمیق تری به آنچه در بالا انجام داده ایم خواهیم داشت.

<p align="center">
    <a href="https://github.com/shayanheidari01/rubika/blob/master/docs/Install-Guide.md">
        صفحه بعدی
    </a>
</p>
