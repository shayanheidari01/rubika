# مستندات کلاس `BotClient`

کلاس `BotClient` هسته اصلی ارتباط با API ربات روبیکا است که برای دریافت، ارسال و مدیریت پیام‌ها، فایل‌ها، وب‌هوک و دیگر عملیات‌های مربوط به بات استفاده می‌شود.

---

## 📌 شروع سریع

```python
client = BotClient(token="YOUR_TOKEN")
await client.start()
```

---

## 🧠 ویژگی‌ها

### 📬 ارسال پیام

```python
await client.send_message(chat_id="12345", text="سلام دنیا!")
```

### 🖼 ارسال فایل، عکس، استیکر و غیره

```python
await client.send_file(chat_id="12345", file="path/to/file.jpg", type="Image")
```

### 📍 ارسال موقعیت مکانی

```python
await client.send_location(chat_id="12345", latitude=35.7, longitude=51.4)
```

### ☎️ ارسال مخاطب

```python
await client.send_contact(chat_id="12345", first_name="علی", last_name="رضایی", phone_number="0912XXXXXXX")
```

---

## 🔄 دریافت آپدیت‌ها

### دریافت با Polling:

```python
updates = await client.get_updates()
```

### دریافت با Webhook:

```python
await client.run(webhook_url="https://your.domain/webhook")
```

---

## ⚙️ تنظیم فیلتر و هندلر برای آپدیت‌ها

```python
@client.on_update(TextFilter("سلام"))
async def greeting_handler(client, update):
    await client.send_message(update.chat_id, "سلام! چطوری؟")
```

---

## ✏️ ویرایش و حذف پیام

```python
await client.edit_message_text(chat_id="12345", message_id="abc", text="متن جدید")
await client.delete_message(chat_id="12345", message_id="abc")
```

---

## 💬 نظرسنجی

```python
await client.send_poll(chat_id="12345", question="نظرت چیه؟", options=["عالی", "خوب", "بد"])
```

---

## 🧪 تنظیم دستورات ربات

```python
await client.set_commands([
    {"command": "/start", "description": "شروع"},
    {"command": "/help", "description": "راهنما"},
])
```

---

## 🌐 تنظیم Webhook

```python
await client.update_bot_endpoints(url="https://your.domain/webhook", endpoint_type="ReceiveUpdate")
```

---

## 🧼 پایان اجرای بات

```python
await client.stop()
await client.close()
```

---

---

## 🧼 نمونه کدها
- [استفاده در حالت لانگ پولینگ](https://github.com/shayanheidari01/rubika/blob/master/examples/example.py)
- [حالت وب هوک](https://github.com/shayanheidari01/rubika/blob/master/examples/use_webhook.py)
- [تست متدها](https://github.com/shayanheidari01/rubika/blob/master/examples/test_bot_api.py)
- [ربات هوش مصنوعی](https://github.com/shayanheidari01/rubika/blob/master/examples/ai.py)


---

## 📚 اطلاعات بیشتر

برای اطلاعات دقیق‌تر، به کد کامل کلاس `BotClient` در مخزن مراجعه نمایید.
