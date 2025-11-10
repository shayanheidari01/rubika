from rubpy import BotClient
from rubpy.bot import filters
from rubpy.bot.models import Update

app = BotClient("BOT_TOKEN")


TEST_TEXT = """🎉 **تست کامل Markdown** 🚀

این یک متن __ایتالیک__ و این هم --زیرخط دار-- است. 
همچنین می‌توانیم ~~خط خورده~~ و ||اسپویلر|| داشته باشیم! 😎

> این یک **quote** چند خطی است 💬
> که شامل __فرمت‌های__ مختلف می‌شود
> و حتی `کد` هم دارد! 🔥

**لیست امکانات:**
• کد تک خطی: `print("Hello")` 
• لینک: [روبیکا](https://rubika.ir) 🌐
• ایموجی: 🎨 🎭 🎪 🎯 🎲

```python
def test_markdown():
    return "این یک بلوک کد است"
```

__نکته مهم:__ تمام فرمت‌ها با هم ترکیب می‌شوند! ✨
**~~ترکیب فرمت‌ها~~** و ||**اسپویلر بولد**|| 🎁

این برای تست کامل پردازش Markdown در کتابخانه روبپای است. 🎊"""

@app.on_update(filters.text, filters.private)
async def markdown_test(client, update: Update):
    await update.reply(TEST_TEXT)

@app.on_update(filters.text, filters.group)
async def markdown_test(client, update: Update):
    await update.reply(TEST_TEXT + f"\n\n[منشن کردن کاربر در گروه]({update.new_message.sender_id})")

app.run()