<p align="center">
    <a href="github.address">
        <img src="https://upcdn.io/W142hJk/thumbnail/demo/4mrDXtYPJA.png.crop" alt="Rubpy" width="128">
    </a>
    <br>
    <b>Rubika API Framework for Python</b>
    <br>
    <a href="https://github.com/shayanheidari01/rubika">
        Homepage
    </a>
    •
    <a href="https://github.com/shayanheidari01/rubika/raw/master/docs/rubpy-documents.pdf">
        Documentation
    </a>
    •
    <a href="https://pypi.org/project/rubpy/#history">
        Releases
    </a>
    •
    <a href="https://t.me/rubika_library">
        News
    </a>
</p>

## Rubpy

> Elegant, modern and asynchronous Rubika API framework in Python for users and bots
# For Bots:
___
```python
from rubpy import Bot

app = Bot('token')

async def my_bot(bot):
    me = await bot.getMe()
    print(me)

app.run(my_bot)
```
**OR**
```python
from rubpy import Bot

app = Bot('token')

async def my_bot(bot):
    data = bot.sendMessage('chat_id', 'text')
    print(await data)

app.run(my_bot)
```
___
# Accounts
``` python
from rubpy import Client

app = Client('MY-AUTH')

@app.handler
async def my_bot(bot, message):
    await message.reply('``Hello`` __from__ **Rubpy**!')

```

**Another example:**
``` python
from rubpy import Client

app = Client("my_account_auth")

async def my_bot(bot):
    await bot.sendText('object_guid', '``Hello`` __from__ **Rubpy**!')

app.run(my_bot)

```

**Rubpy** is a modern, elegant and asynchronous framework. It enables you to easily interact with the main Rubika API through a user account (custom client) or a bot
identity (bot API alternative) using Python.


### Key Features

- **Ready**: Install Rubpy with pip and start building your applications right away.
- **Easy**: Makes the Rubika API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Fast**: Boosted up by pycryptodome, a high-performance cryptography library written in C.
- **Async**: Fully asynchronous (also usable synchronously if wanted, for convenience).
- **Powerful**: Full access to Rubika's API to execute any official client action and more.

### Installing

``` bash
pip3 install rubpy==5.1.0
```
