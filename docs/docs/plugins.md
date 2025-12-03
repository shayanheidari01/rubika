# سیستم پلاگین‌های Rubpy

## چرا پلاگین؟
- جداسازی قابلیت‌های اختیاری از هسته‌ی بات
- قابل اشتراک‌گذاری و نصب از PyPI (با `pip install`)
- بارگذاری خودکار از طریق **Entry Point** های استاندارد پایتون

## مفاهیم کلیدی
- `Plugin`: کلاس پایه در `rubpy.plugins.base.Plugin`
- `PluginMeta`: متادیتای انسانی شامل نام، نسخه و توضیحات
- `PluginManager`: مسئول کشف، فعال‌سازی و غیرفعال‌سازی پلاگین‌ها
- گروه Entry Point پیش‌فرض: `rubpy.plugins`

## ساخت یک پلاگین ساده
```python
# my_echo_plugin/plugin.py
from rubpy.plugins import Plugin, PluginMeta
from rubpy.bot.filters import text

class EchoPlugin(Plugin):
    meta = PluginMeta(
        name="rubpy-echo",
        version="1.0.0",
        description="Echo incoming private messages",
        author="Rubpy Dev",
        homepage="https://github.com/...",
    )

    def setup(self):
        @self.bot.on_update(text)
        async def echo(client, update):
            await client.send_message(update.chat_id, update.new_message.text)
```

## بسته‌بندی برای PyPI
### 1. ساختار پروژه
```
my-echo-plugin/
├─ pyproject.toml  # یا setup.cfg
override ok
├─ README.md
└─ my_echo_plugin/
   └─ plugin.py
```

### 2. تعریف Entry Point
مثال `pyproject.toml`:
```toml
[project]
name = "rubpy-echo-plugin"
version = "1.0.0"
dependencies = ["rubpy>=7.2.7"]

[project.entry-points."rubpy.plugins"]
# مقدار سمت چپ شناسه قابل‌خواندن، سمت راست مسیر کلاس
rubpy_echo = "my_echo_plugin.plugin:EchoPlugin"
```
یا معادل در `setup.py`:
```python
setup(
    ...,
    entry_points={
        "rubpy.plugins": [
            "rubpy_echo = my_echo_plugin.plugin:EchoPlugin",
        ]
    }
)
```
با انتشار بسته در PyPI، کاربران فقط با `pip install rubpy-echo-plugin` آن را در دسترس Rubpy قرار می‌دهند.

## فعال‌سازی در بات
```python
from rubpy.bot import BotClient

bot = BotClient(
    token="...",
    auto_enable_plugins=True,
    plugins=["rubpy_echo"],  # اختیاری: فهرست شناسه‌هایی که باید فعال شوند
)

bot.run()
```
نکات:
1. اگر `plugins` مشخص نشود، `PluginManager` همه‌ی پلاگین‌های کشف‌شده از Entry Point ها را فعال می‌کند.
2. می‌توانید در زمان اجرا نیز پلاگین ثبت کنید:
```python
bot.register_plugin(EchoPlugin, name="rubpy_echo")
await bot.enable_plugins(["rubpy_echo"])
```
3. برای غیرفعال کردن:
```python
await bot.disable_plugins(["rubpy_echo"])
```

## تست محلی قبل از انتشار
- پلاگین را در محیط مجازی نصب editable کنید: `pip install -e .`
- بات را با `auto_enable_plugins=True` اجرا کنید تا پلاگین جدید لود شود.
- لاگ‌های Rubpy برای وضعیت فعال‌سازی هشداری ثبت می‌کنند.

## بهترین تجربه انتشار
1. **نسخه‌گذاری معنایی** و توضیحات کامل در PyPI
2. **README** شامل نحوه فعالسازی در Rubpy
3. **لایسنس سازگار** با LGPLv3
4. استفاده از CI برای اجرای lint/test پلاگین

با این ساختار، Rubpy به شکل بومی از اکوسیستم PyPI پشتیبانی می‌کند و توسعه‌دهندگان می‌توانند قابلیت‌های خود را به‌صورت پلاگین منتشر کنند.

## مثال عملی آماده
- فایل `examples/plugin_echo.py` یک پلاگین «Echo» را inline ثبت می‌کند و نشان می‌دهد چگونه می‌توان بدون انتشار در PyPI آن را تست کرد.
- اجرای نمونه:
  ```bash
  export RUBPY_BOT_TOKEN="توکن_ربات"
  python examples/plugin_echo.py
  ```
- این مثال پیکربندی `auto_enable_plugins=True` و متدهای `register_plugin`, `enable_plugins` را در عمل نشان می‌دهد.

## قابلیت‌های پیشرفته
- **پیکربندی سفارشی:** در `BotClient(..., plugin_configs={"plugin_id": {...}})` می‌توانید مقادیر پیش‌فرض `PluginMeta.default_config` را override کنید. در خود پلاگین از `self.get_config` یا متد `configure` برای اعتبارسنجی استفاده کنید.
- **وابستگی بین پلاگین‌ها:** فیلد `PluginMeta.dependencies` لیستی از شناسه پلاگین‌های مورد نیاز است؛ پیش از فعال‌سازی پلاگین اصلی، این وابستگی‌ها به‌صورت خودکار فعال می‌شوند.
- **پلاگین‌های میانگذر/تجربی:** با تعریف `@bot.middleware()` داخل `setup` می‌توانید pipeline را دستکاری یا لاگ‌گیری کنید (نمونه‌ی `LoggerPlugin` در مثال).
- **دسترسی‌ها:** هر پلاگین هنگام ساخت نمونه، شیء `BotClient` را دریافت می‌کند؛ بنابراین می‌تواند به تمام متدهای عمومی Rubpy (ارسال پیام، مدیریت فایل، فیلترها، مدل‌ها، `middlewares`, `on_update`) دسترسی داشته باشد و حتی با زیرسیستم‌هایی مثل `rubpy.methods` یا `rubpy.enums` مستقیماً کار کند. تنها محدودیت، رعایت API عمومی کتابخانه است.
