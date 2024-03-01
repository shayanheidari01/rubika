### راه اندازی پروژه

ما به تازگی [Rubpy](/aboutinstall) را نصب کرده ایم. در این صفحه ما در مورد کارهایی که برای راه اندازی یک پروژه با چارچوب باید انجام دهید صحبت خواهیم کرد.


### پیکربندی

با در دست داشتن کلید token , auth اکنون می‌توانیم پیکربندی پروژه Rubpy را شروع کنیم: با استفاده از پارامترهای token و auth کلاس Client، کلید token , auth خود را به Rubpy منتقل کنید:



```python
from rubpy import Client

token = 'abcdef'
auth = "asdef"

app = Client("my_account", token=token, auth=auth)

```