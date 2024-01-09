# ثبت نام و ورود
#### جهت استفاده از کتابخانه باید یک نشست در حساب کاربری شما در روبیکا ایجاد شود، برای ثبت نام یا ورود با حساب کاربری خود در روبیکا پای و ایجاد نشست جدید برای استفاده از روبیکا پای این آموزش را دنبال کنید.
___

1. ابتدا برای ثبت نام باید یک فایل با نام ``login.py`` ایجاد کنید.
2. با ویرایشگر کد خود، کد زیر را در فایل وارد کنید و ذخیره کنید.
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
3. حالا با دستور ``python3 login.py`` در ترمینال خود فایل را اجرا کنید.
4. حالا شما میتوانید عملیات وارد شدن به حساب کاربری خود را کامل کنید. 
5. بعد از کامل شدن ثبت نام و وارد کردن کد، فایل را ببندید و مجددا اجرا کنید.
6. حالا ربات روی حساب کاربری شما اجرا شده است.
<p align="center">
    <a href="https://github.com/shayanheidari01/rubika/blob/master/docs/Handling-Updates.md">
        صفحه بعدی
    </a>
  •
  <a href="https://github.com/shayanheidari01/rubika/blob/master/docs/Project-Setup.md">
        صفحه قبلی
    </a>
</p>
