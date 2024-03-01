چند مرحله بعدی به عنوان یک شروع سریع برای دیدن Rubpy در عمل در اسرع وقت است.

### نصب

نحوه‌ی نصب کتابخانه

```bash
pip install -u rubpy
```



### مرور سریع


```python 
from rubpy import Client, filters, utils
from rubpy.types import Updates

bot = Client(name='rubpy')

@bot.on_message_updates(filters.text)
async def updates(update: Updates):
    print(update)
    await update.reply(utils.Code('hello') + utils.Underline('from') + utils.Bold('rubpy'))

bot.run()
```


### لذت بردن از API 


 این فقط یک مرور سریع بود. در چند صفحه بعدی مقدمه، ما نگاهی عمیق تر به انچه که ما فقط در بالا انجام داده ایم.

اگر شما احساس مشتاق به ادامه شما می توانید میانبر به Invoking روش را و دوباره بعدا برای یادگیری برخی از جزئیات بیشتر.'
