# کلاینت Rubpy
شما از این به بعد قرار است اطلاعات دقیق تری از روبیکاپای به دست آورید، حالا کلاس Client را بررسی میکنیم.
```python
from rubpy import Client
from asyncio import run

async def main():
  async with Client("my_account") as client:
    app.send_message("me", "Hi!")

run(main())
```
