# راهنمای نصب Rubpy

کتابخانه **Rubpy** یک فریم‌ورک مدرن پایتون برای ساخت ربات‌های پیام‌رسان **روبیکا** است. برای استفاده از آن، باید **پایتون ۳** و ابزار **pip** را روی سیستم خود نصب داشته باشید. توصیه می‌کنیم از آخرین نسخه‌های پایدار استفاده کنید.

---

## 🧰 نصب Rubpy

ساده‌ترین روش برای نصب یا به‌روزرسانی Rubpy به آخرین نسخه پایدار، استفاده از دستور زیر است:

```bash
pip3 install -U rubpy
```


## 🚀 نسخه توسعه (Bleeding Edge)

برای نصب آخرین نسخه توسعه‌یافته از مخزن گیت‌هاب:

```bash
pip3 install -U https://github.com/shayanheidari/rubika/archive/master.zip
```

---

## ✅ اطمینان از نصب موفق

برای اطمینان از اینکه Rubpy به درستی نصب شده است، یک شل پایتون باز کرده و کد زیر را اجرا کنید:

```python
import rubpy
print(rubpy.__version__)
```

اگر خطایی دریافت نکردید، نصب موفقیت‌آمیز بوده است.

---

## 💡 توسعه‌دهنده

این پروژه توسط [Shayan Heidari](https://github.com/shayanheidari01) توسعه داده شده است. خوشحال می‌شویم اگر باگ‌ها، پیشنهادات و مشارکت‌های خود را از طریق **Issues** یا **Pull Requests** با ما در میان بگذارید.

---

## 📬 ارتباط

برای دریافت نکات برنامه‌نویسی و اخبار Rubpy، می‌توانید در خبرنامه ما [در تلگرام](https://t.me/rubikapy) عضو شوید.

---

## 🛡 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است. برای اطلاعات بیشتر به فایل [LICENSE](./LICENSE) مراجعه کنید.


- [متدهای کلاس rubpy.Client](https://github.com/shayanheidari01/rubika/blob/master/docs/client_methods.md)
- [متدهای کلاس rubpy.types.Update](https://github.com/shayanheidari01/rubika/blob/master/docs/update_methods.md)
- [مستندات rubpy.BotClient](https://github.com/shayanheidari01/rubika/blob/master/docs/bot_client.md)
