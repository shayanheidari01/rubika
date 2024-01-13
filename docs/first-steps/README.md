# شروع سریع
چند مرحله سریعتر برای مشاهده عملکرد rubpy اقدام میکنیم.
## دریافت و نصب rubpy واقعا سریع است
1. نصب کتابخانه با `pip3 install -U rubpy`
2. می‌توانید از auth و private_key خود استفاده کنید و یا با استفاده از شماره تلفن خود وارد حساب کاربری خود شوید.
3. ویرایشگر کد خود را باز کنید و کد زیر را در آن وارد کنید:
   ```python
   import asyncio
   from rubpy import Client

   auth = None
   private_key = None

   async def main():
       async with Client('my_account', auth=auth, private_key=private_key) as app:
           await app.send_message('me', 'Greetings from **rubpy**!')

asyncio.run(main())
   ```
4. وارد کردن auth و private_key اجباری نیست، در صورتی که برابر None باشد مستقیما باید با شماره تلفن خود وارد شوید.
5. فایل را به عنوان `hello.py`  ذخیره کنید.
6. اسکریپت را با `python3 hello.py` اجرا کنید.
7. در ترمینال در صورتی که auth و private_key خود را وارد نکرده‌اید مراحل وارد شدن به حساب کاربری خود با شماره تلفن را دنبال کنید.
8. حالا یک پیام برای خودتان ارسال کردید.
