# شروع سریع
#### چند مرحله سریع تر شروع میکنیم، برای دیدن سرعت و عمکلکرد فریمورک روبیکا پای


## سرعت باورنکردنی روبیکا پای

1. کتابخانه را با دستور ```pip install -U  rubpy``` نصب کنید
2. ویرایشگر کد خود را باز کنید و تیکه کد زیر را در آن وارد نمایید
```python
from rubpy import Client, filters, utils
from rubpy.types import Updates

bot = Client(name='rubpy')

@bot.on_message_updates(filters.text)
async def updates(update: Updates):
    print(update)
    await update.reply(utils.Code('hello') + utils.Underline('from') + utils.Bold('rubpy'))

bot.run()
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
