ماژول `rubpy.bot.filters` مجموعه‌ای از فیلترها را برای مدیریت و فیلتر کردن آپدیت‌های ربات فراهم می‌کند.
هر فیلتر کلاس/تابعی است که متد `check` (async) را پیاده‌سازی می‌کند و هنگام دریافت آپدیت بررسی می‌کند که آیا هندلر باید اجرا شود یا خیر.

## استفادهٔ کلی

```python
from rubpy import BotClient
from rubpy.bot import filters

bot = BotClient("your_bot_token")

@bot.on_update(filters.text("hello"))
async def handle_hello(c, update):
    await c.send_message(update.chat_id, "Hello!")
```

---

## طراحی کلی فیلترها

* همهٔ فیلترها **آسینک** هستند و متد `check(update)` را پیاده‌سازی می‌کنند.
* یک فیلتر هنگام استفاده می‌تواند به‌صورت کلاس (نمونه‌سازی داخلی) یا نمونهٔ آماده به دکوراتور پاس داده شود.
* چند فیلتر را می‌توان به‌صورت positional به `@on_update(...)` پاس داد تا همگی با هم بررسی شوند (AND منطقی).

## `text`

| پارامتر       |             نوع | توضیحات                                                   |
| ------------- | --------------: | --------------------------------------------------------- |
| `pattern`     | `Optional[str]` | متن یا الگوی regex (اگر None یعنی هر متنی)                |
| `regex`       |          `bool` | آیا `pattern` به‌صورت regex تفسیر شود؟ (پیش‌فرض False)    |
| `ignore_case` |          `bool` | نادیده گرفتن بزرگ/کوچک بودن حروف در مقایسه (پیش‌فرض True) |

**شرح کوتاه:** فیلتر بر اساس متن پیام؛ از تطبیق دقیق یا regex پشتیبانی می‌کند.

**بازگشت:** نمونه‌ی فیلتر (قابل استفاده در `@on_update`)

**مثال‌ها:**

```python
@bot.on_update(filters.text)  # هر متنی
async def any_text(c, u): ...

@bot.on_update(filters.text("hello"))  # تطبیق دقیق
async def exact(c, u): ...

@bot.on_update(filters.text(r"^/start", regex=True))  # regex
async def start_cmd(c, u): ...
```

**نکته:** اگر `pattern` خالی باشد و `regex=False`، فیلتر فقط چک می‌کند که پیام متنی وجود دارد.

---

## `commands`

| پارامتر    |   نوع | توضیحات      |                         |
| ---------- | ----: | ------------ | ----------------------- |
| `commands` | \`str | List\[str]\` | نامِ فرمان(ها) بدون `/` |

**شرح کوتاه:** پیام‌هایی که با دستور مشخص شروع می‌شوند (مثلاً `/start`).

**مثال:**

```python
@bot.on_update(filters.commands("start"))
async def start(c, u): ...

@bot.on_update(filters.commands(["help","about"]))
async def help_or_about(c, u): ...
```

**نکته:** این فیلتر معمولاً متن پیام را به صورت tokenized بررسی می‌کند تا فرمان در ابتدای متن باشد.

---

## `update_type`

| پارامتر |   نوع | توضیحات      |                                                         |
| ------- | ----: | ------------ | ------------------------------------------------------- |
| `types` | \`str | List\[str]\` | یک یا چند مقدار از `UpdateTypeEnum` یا معادل رشته‌ای آن |

**شرح کوتاه:** فیلتر براساس نوع آپدیت (مثلاً `NewMessage`, `UpdatedMessage`, `InlineMessage`).

**مثال:**

```python
@bot.on_update(filters.update_type("NewMessage"))
async def newmsg(c, u): ...

@bot.on_update(filters.update_type(["NewMessage","InlineMessage"]))
async def multi(c, u): ...
```

---

## `private`

| پارامتر | نوع | توضیحات      |
| ------- | --: | ------------ |
| —       |   — | بدون پارامتر |

**شرح کوتاه:** پاس کردن تنها زمانی که آپدیت از یک چت خصوصی (user) باشد.

**مثال:**

```python
@bot.on_update(filters.private)
async def priv(c,u): ...
```

---

## `group`

| پارامتر | نوع | توضیحات      |
| ------- | --: | ------------ |
| —       |   — | بدون پارامتر |

**شرح کوتاه:** پاس کردن تنها زمانی که پیام از گروه باشد.

**مثال:**

```python
@bot.on_update(filters.group)
async def grp(c,u): ...
```

---

## `channel`

| پارامتر | نوع | توضیحات      |
| ------- | --: | ------------ |
| —       |   — | بدون پارامتر |

**شرح کوتاه:** پاس کردن تنها زمانی که پیام از کانال باشد.

**مثال:**

```python
@bot.on_update(filters.channel)
async def chl(c,u): ...
```

---

## `bot`

| پارامتر | نوع | توضیحات      |
| ------- | --: | ------------ |
| —       |   — | بدون پارامتر |

**شرح کوتاه:** پیام‌هایی که فرستنده‌شان از نوع `Bot` است.

**مثال:**

```python
@bot.on_update(filters.bot)
async def from_bot(c,u): ...
```

---

## `chat`

| پارامتر    |   نوع | توضیحات      |                                             |
| ---------- | ----: | ------------ | ------------------------------------------- |
| `chat_ids` | \`str | List\[str]\` | یک شناسه یا لیست شناسه‌های چت که اجازه دارد |

**شرح کوتاه:** محدود کردن اجرای هندلر به یک یا چند `chat_id` مشخص.

**مثال:**

```python
@bot.on_update(filters.chat("b0_test_chat"))
async def test(c,u): ...

@bot.on_update(filters.chat(["b0_admin","b0_mod"]))
async def admin_mod(c,u): ...
```

---

## `button`

| پارامتر   |    نوع | توضیحات                                         |
| --------- | -----: | ----------------------------------------------- |
| `pattern` |  `str` | متن یا الگوی شناسه دکمه                         |
| `regex`   | `bool` | آیا pattern به‌صورت regex باشد؟ (پیش‌فرض False) |

**شرح کوتاه:** فیلتر کلیک روی دکمه‌ها (callback / button id) — تطبیق دقیق یا regex.

**مثال:**

```python
@bot.on_update(filters.button("btn_123"))
async def b123(c,u): ...

@bot.on_update(filters.button(r"btn_\d+", regex=True))
async def numbered(c,u): ...
```

---

## `forward`

| پارامتر | نوع | توضیحات      |
| ------- | --: | ------------ |
| —       |   — | بدون پارامتر |

**شرح کوتاه:** پاس می‌شود اگر پیام از جایی فوروارد شده باشد (`forwarded_from` وجود داشته باشد).

**مثال:**

```python
@bot.on_update(filters.forward)
async def fwd(c,u): ...
```

---

## `replied`

| پارامتر | نوع | توضیحات      |
| ------- | --: | ------------ |
| —       |   — | بدون پارامتر |

**شرح کوتاه:** بررسی اینکه آیا پیام روی یک پیام دیگر ریپلای شده یا خیر.

**مثال:**

```python
@bot.on_update(filters.replied)
async def is_replieds(c,u): ...
```

---

## `is_edited`

| پارامتر | نوع | توضیحات      |
| ------- | --: | ------------ |
| —       |   — | بدون پارامتر |

**شرح کوتاه:** فیلتر پیام‌های ویرایش‌شده (`is_edited == True` یا نوع `UpdatedMessage`).

**مثال:**

```python
@bot.on_update(filters.is_edited)
async def edited(c,u): ...
```

---

## `sender_type`

| پارامتر |   نوع | توضیحات      |                                             |
| ------- | ----: | ------------ | ------------------------------------------- |
| `types` | \`str | List\[str]\` | نوع/انواع فرستنده (مثلاً `"User"`, `"Bot"`) |

**شرح کوتاه:** فیلتر بر اساس `sender_type` پیام.

**مثال:**

```python
@bot.on_update(filters.sender_type("User"))
async def from_user(c,u): ...

@bot.on_update(filters.sender_type(["Bot","Channel"]))
async def bot_or_channel(c,u): ...
```

---

## `has_aux_data`

| پارامتر | نوع | توضیحات      |
| ------- | --: | ------------ |
| —       |   — | بدون پارامتر |

**شرح کوتاه:** پاس می‌شود اگر پیام `aux_data` داشته باشد (مفید برای دکمه‌ها/payloadها).

**مثال:**

```python
@bot.on_update(filters.has_aux_data)
async def aux(c,u): ...
```

---

## `file`

| پارامتر | نوع | توضیحات      |
| ------- | --: | ------------ |
| —       |   — | بدون پارامتر |

**شرح کوتاه:** پیام‌هایی که پیوست فایل دارند (`message.file`).

**مثال:**

```python
@bot.on_update(filters.file)
async def new_file(c,u): ...
```

---

## `location`

| پارامتر | نوع | توضیحات      |
| ------- | --: | ------------ |
| —       |   — | بدون پارامتر |

**شرح کوتاه:** پیام‌هایی که لوکیشن دارند (`message.location` یا `live_location`).

**مثال:**

```python
@bot.on_update(filters.location)
async def loc(c,u): ...
```

---

## `sticker`

| پارامتر | نوع | توضیحات      |
| ------- | --: | ------------ |
| —       |   — | بدون پارامتر |

**شرح کوتاه:** پیام‌هایی که استیکر دارند (`message.sticker`).

**مثال:**

```python
@bot.on_update(filters.sticker)
async def stk(c,u): ...
```

---

## `contact_message`

| پارامتر | نوع | توضیحات      |
| ------- | --: | ------------ |
| —       |   — | بدون پارامتر |

**شرح کوتاه:** پیام‌هایی که شامل کانتکت هستند (`message.contact_message`).

**مثال:**

```python
@bot.on_update(filters.contact_message)
async def contact(c,u): ...
```

---

## `poll`

| پارامتر | نوع | توضیحات      |
| ------- | --: | ------------ |
| —       |   — | بدون پارامتر |

**شرح کوتاه:** پیام‌هایی که نظرسنجی (poll) دارند (`message.poll`).

**مثال:**

```python
@bot.on_update(filters.poll)
async def poll_msg(c,u): ...
```

---

## `live_location`

| پارامتر | نوع | توضیحات      |
| ------- | --: | ------------ |
| —       |   — | بدون پارامتر |

**شرح کوتاه:** پیام‌هایی که موقعیت زنده (`live_location`) دارند.

**مثال:**

```python
@bot.on_update(filters.live_location)
async def live_loc(c,u): ...
```

---

## ترکیب فیلترها (Multi filters)

چند فیلتر را می‌توان کنار هم قرار داد؛ همه باید پاس شوند (منطق AND):

```python
@bot.on_update(filters.private, filters.commands('start'))
async def welcome(c,u):
    await u.reply("Welcome to private start!")
```

### استفاده پیشرفته:
ترکیب فیلترهای OR و AND.

```python
@bot.on_update(filters.commands('hello') & (filters.private | filters.group))
async def hello_world(c,u):
    await u.reply("Hello, World!")
```

---

# فیلتر `states`

فیلتر `states` یک کلاس برای مدیریت **وضعیت مکالمه (conversation state)** در ربات است.
این فیلتر بررسی می‌کند که آیا به‌روزرسانی (`update`) مربوط به **یک state مشخص** است یا نه، بدون نیاز به کتابخانه یا مدیریت‌کننده خارجی.

---

## 🚀 مثال‌های استفاده

### 1. تعیین وضعیت بعد از دستور `/start`

```python
@bot.on_message(text("/start"))
async def start_handler(client, message):
    await message.reply("سلام! لطفاً نام خود را وارد کنید.")
    states.set(message.user_id, "waiting_for_name")
```

---

### 2. پردازش ورودی بر اساس وضعیت

```python
@bot.on_message(states("waiting_for_name"))
async def name_handler(client, message):
    await message.reply(f"خوشبختم {message.text}! سن خود را وارد کنید.")
    states.set(message.user_id, "waiting_for_age")
```

---

### 3. انتقال بین وضعیت‌ها

```python
@bot.on_message(states("waiting_for_age"))
async def age_handler(client, message):
    await message.reply(f"عالی! شما {message.text} ساله هستید.")
    states.clear(message.user_id)  # پایان جریان مکالمه
```

---

### 4. بررسی وضعیت فعلی کاربر

```python
user_state = states.get(message.user_id)
if user_state == "waiting_for_age":
    await message.reply("شما هنوز در حالت وارد کردن سن هستید.")
```

---

### 🧩 نکات کلیدی

* از **رشته‌های کوتاه و گویا** برای وضعیت‌ها استفاده کنید (`"waiting_for_email"`, `"awaiting_confirmation"`).
* همیشه بعد از پایان جریان مکالمه، وضعیت را با `clear` پاک کنید تا حافظه اضافه مصرف نشود.
* برای مدیریت جریان‌های پیچیده، می‌توانید وضعیت‌ها را گروه‌بندی کنید (`"reg:name"`, `"reg:age"`, `"reg:done"`).

---

## نکات پیاده‌سازی و بهترین تمرین‌ها

* متد `check(update)` در هر فیلتر **آسینک** باشد تا بتواند منابع IO (مثلاً دیتابیس یا شبکه) را نیز چک کند.
* برای فیلترهای Regex، استفاده از کامپایل کردن الگو (`re.compile`) در سازندهٔ فیلتر باعث افزایش کارایی می‌شود.
* هنگام بررسی متن، همیشه `None` بودن فیلدها را چک کنید تا از `AttributeError` جلوگیری شود.
* اگر نیاز به فیلتر stateful دارید (مثلاً محدودیت نرخ برای کاربر)، پیاده‌سازی را به گونه‌ای انجام دهید که thread-safe یا compatible با async باشد (مثلاً استفاده از async locks یا external store مثل Redis).
* برای تست، فیلترها را به‌صورت جداگانه unit-test کنید با نمونه‌های `Update`/`InlineMessage` مصنوعی.

---

## FAQ

**۱) آیا فیلترها می‌توانند async I/O انجام دهند؟**
بله — `check` آسینک است و می‌تواند درخواست‌های دیتابیسی یا شبکه‌ای داشته باشد.

**۲) ترتیب بررسی فیلترها چگونه است؟**
فیلترها به ترتیب قرارگیری در دکوراتور بررسی می‌شوند؛ اولین فیلتر که `False` برگرداند از اجرای هندلر جلوگیری می‌کند.

**۳) آیا OR ترکیب فیلترها پشتیبانی می‌شود؟**
در نسخهٔ پایه ترکیب به صورت AND است. اگر لازم است، می‌توانید یک helper بنویسید که OR را پیاده‌سازی کند یا فیلتر جدیدی بسازید.