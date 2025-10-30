این بخش شامل نمونه‌های کاربردی برای کار با `rubpy` است. هر مثال یک فایل مجزا در نظر گرفته شده است. دقت کنید که مثال های این بخش صرفا برای استفاده از بخش `rubpy.Client` یا همان حساب های کاربری هستند و برای استفاده از بات ها اصلا مناسب نیستند. برای مثال های بات به صفحه مربوطه مراجعه کنید در غیر این صورت مثال ها را مطالعه کنید.

---

## سلام دنیا

فایل: **`hello_world.py`**

```python
from rubpy import Client

# Create a new Client instance
app = Client("session-name")


async def main():
    # Start client
    await app.start()

    # Send a message, Markdown is enabled by default
    await app.send_message("me", "Hi there! I'm using **Rubpy**")

    # Close client
    await app.disconnect()


import asyncio
asyncio.run(main())
```

---

## بازتاب پیام

فایل: **`echo_bot.py`**

```python
from rubpy import Client, filters

app = Client("session-name")


@app.on_message_updates(filters.text, filters.private)
async def echo(client, update):
    await update.reply(update.text)


app.run()  # Automatically start()
```

---

# نکات
- کتابخانه روبپای را در دو حالت sync و async میتوان استفاده کرد.
- پس از ورود به حساب کاربری، یک نشست در حساب ایجاد میشود، پس از اتمام مراحل ورود به حساب، یک فایل با فرمت .rp در کنار فایل ربات شما ذخیره میشود. این یعنی پس از آن نیازی به ورود مجدد به حساب خود ندارید.


--- 

## دریافت لیست کامل اعضا

فایل: **`get_all_members.py`**

```python
from rubpy import Client

OBJECT_GUID = ''  # GUID گروه یا کانال موردنظر

with Client('get_all_members') as app:
    has_continue = True
    next_start_id = None
    total_members = 0

    while has_continue:
        response = app.get_members(OBJECT_GUID, start_id=next_start_id)

        if not response:
            break  # اگر پاسخ خالی بود، حلقه متوقف شود

        next_start_id = response.next_start_id
        has_continue = response.has_continue
        members = response.in_chat_members or []

        for member in members:
            # print(member)
            total_members += 1

    print("Total members:", total_members)
```

--- 

## کانتکست منیجر

فایل: **`use_context_manager.py`**

```python
# Use async
async with Client('my_session') as app:
    print(await app.get_me())

# Use sync
with Client('my_session') as app:
    print(app.get_me())
```

## استفاده همزمان

فایل: **`no_async_rubpy.py`**

```python
# استفاده از کانتکست منیجر به صورت همزمان
with Client('my_session') as app:
    print(app.get_me())

# بدون کانتکست منیجر
app = Client('my_session')

app.start()

app.send_message("me", "Hello from rubpy!")

app.disconnect()
```