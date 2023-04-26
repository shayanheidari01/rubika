# کلاینت Rubpy
شما از این به بعد قرار است اطلاعات دقیق تری از روبیکاپای به دست آورید، حالا کلاس Client را بررسی میکنیم.
```python
from rubpy import Client
from asyncio import run

async def main():
  async with Client("my_account") as client:
    await client.send_message("me", "Hi!")

run(main())
```
# جزئیات
`class rubpy.Client`
  کلاینت روبیکاپای، ابزار اصلی برای تعامل با روبیکا است.
      `Parameters:`
      - session(`str`) - یک نام برای کلاینت به عنوان مثال: "my_account".
      - 
