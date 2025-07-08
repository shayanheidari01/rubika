<p align="center">
  <a href="https://github.com/shayanheidari01/rubika">
    <img src="https://raw.githubusercontent.com/shayanheidari01/rubika/master/icon.png" width="128" alt="Rubpy Logo" />
  </a>
  <br><br>
  <strong><font size="+2">Rubpy</font></strong><br>
  <em>Asynchronous & elegant Python framework for the Rubika API</em>
  <br><br>
  <a href="https://github.com/shayanheidari01/rubika">🏠 Homepage</a> •
  <a href="https://github.com/shayanheidari01/rubika/tree/master/docs">📘 Documentation</a> •
  <a href="https://pypi.org/project/rubpy/#history">📦 Releases</a> •
  <a href="https://t.me/rubikapy">🗞 News</a>
</p>

---

## 🌟 Rubpy

> **Modern. Elegant. Asynchronous.**  
> A clean Pythonic interface to interact with Rubika's API — for both **users** and **bots**.

---

### 🚀 Async Example
```python
from rubpy import Client, filters
from rubpy.types import Update

bot = Client(name='rubpy')

@bot.on_message_updates(filters.text)
async def updates(update: Update):
    print(update)
    await update.reply('`hello` __from__ **rubpy**')
  

bot.run()
```

**Minimal Async:**
```python
from rubpy import Client
import asyncio

async def main():
    async with Client(name='rubpy') as bot:
        result = await bot.send_message('me', '`hello` __from__ **rubpy**')
        print(result)

asyncio.run(main())
```

---

### ⚡ Sync Example
```python
from rubpy import Client

bot = Client('rubpy')

@bot.on_message_updates()
def updates(message):
    message.reply('`hello` __from__ **rubpy**')

bot.run()
```

**Minimal Sync:**
```python
from rubpy import Client

with Client(name='rubpy') as client:
    result = client.send_message('me', '`hello` __from__ **rubpy**')
    print(result)
```

---

### ✨ Why Rubpy?

- 📦 **Ready** — Install with pip and start instantly
- 🧠 **Easy** — Clean, intuitive, and beginner-friendly
- 💅 **Elegant** — Beautifully abstracted low-level details
- 🚀 **Fast** — Powered by high-performance `pycryptodome`
- 🔁 **Async First** — Full async design, with sync support
- 💪 **Powerful** — Everything the official client can do — and more

---

### 📦 Installation

```bash
pip install -U rubpy
```

---

### 📣 Stay Connected

- [Telegram Channel](https://t.me/rubikapy)
- [Project Homepage](https://github.com/shayanheidari01/rubika)
