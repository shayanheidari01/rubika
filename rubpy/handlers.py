import asyncio
import sys
from typing import Type, List, Dict, Any, Optional
from .types import Update

# لیست handlerهای مجاز
AUTHORIZED_HANDLERS = [
    'ChatUpdates',
    'MessageUpdates',
    'ShowActivities',
    'ShowNotifications',
    'RemoveNotifications'
]

def create_handler(
    name: str,
    base: tuple,
    authorized_handlers: List[str] = AUTHORIZED_HANDLERS,
    exception: bool = True,
    **kwargs
) -> Optional[Type['BaseHandlers']]:
    """
    ایجاد دینامیک یک handler بر اساس نام و کلاس پایه.

    پارامترها:
    - name: نام handler.
    - base: کلاس پایه برای handler.
    - authorized_handlers: لیست نام‌های handlerهای مجاز.
    - exception: آیا در صورت غیرمجاز بودن handler خطا پرتاب شود.
    - kwargs: آرگومان‌های اضافی برای تنظیم کلاس.

    خروجی:
    کلاس handler ایجادشده یا None در صورت غیرمجاز بودن.

    خطاها:
    - AttributeError: اگر handler غیرمجاز باشد و exception=True.
    """
    if name in authorized_handlers:
        return type(name, base, {'__name__': name, **kwargs})
    
    if not exception:
        return None
    
    raise AttributeError(f"ماژول فاقد handler با نام '{name}' است")

class BaseHandlers(Update):
    """
    کلاس پایه برای handlerهای سفارشی.

    پارامترها:
    - models: لیست مدل‌های فیلتر.
    - any_handler: آیا هر handler باید اجرا شود.
    - kwargs: آرگومان‌های اضافی.
    """
    __name__ = 'CustomHandlers'

    def __init__(self, *models: Any, any_handler: bool = False, **kwargs) -> None:
        self.__models = models
        self.__any_handler = any_handler

    def is_async(self, value: Any) -> bool:
        """
        بررسی اینکه آیا تابع داده‌شده ناهمگام (async) است.

        پارامترها:
        - value: تابع برای بررسی.

        خروجی:
        True اگر تابع ناهمگام باشد، در غیر این صورت False.
        """
        return asyncio.iscoroutinefunction(value) or (hasattr(value, '__call__') and asyncio.iscoroutinefunction(value.__call__))

    async def __call__(self, update: Dict, *args, **kwargs) -> bool:
        """
        اجرای handler روی آپدیت داده‌شده.

        پارامترها:
        - update: دیکشنری آپدیت.
        - args: آرگومان‌های اضافی موقعیتی.
        - kwargs: آرگومان‌های اضافی کلیدی.

        خروجی:
        True اگر handler باید اجرا شود، در غیر این صورت False.
        """
        self.original_update = update

        if not self.__models:
            return True

        for handler_filter in self.__models:
            # اگر handler_filter یک کلاس باشد، نمونه‌سازی می‌شود
            filter_instance = handler_filter(func=None) if isinstance(handler_filter, type) else handler_filter
            # بررسی ناهمگام یا همگام بودن فیلتر و اجرای آن
            status = await filter_instance(self, result=None) if self.is_async(filter_instance) else filter_instance(self, result=None)

            if status and self.__any_handler:
                return True
            if not status:
                return False

        return True

class Handlers:
    """
    کلاس برای مدیریت و ایجاد handlerهای خاص.
    """
    def __init__(self, name: str) -> None:
        self.__name__ = name

    def __eq__(self, value: object) -> bool:
        """
        بررسی برابری با کلاس پایه handlerها.

        پارامترها:
        - value: مقداری برای بررسی.

        خروجی:
        True اگر برابر با BaseHandlers باشد، در غیر این صورت False.
        """
        return BaseHandlers in getattr(value, '__bases__', ())

    def __dir__(self) -> List[str]:
        """
        دریافت لیست handlerهای مجاز.

        خروجی:
        لیست مرتب‌شده handlerهای مجاز.
        """
        return sorted(AUTHORIZED_HANDLERS)

    def __call__(self, name: str, *args, **kwargs) -> Type['BaseHandlers']:
        """
        فراخوانی handler بر اساس نام.

        پارامترها:
        - name: نام handler.
        - args: آرگومان‌های اضافی موقعیتی.
        - kwargs: آرگومان‌های اضافی کلیدی.

        خروجی:
        کلاس handler ایجادشده.
        """
        return self.__getattr__(name)(*args, **kwargs)

    def __getattr__(self, name: str) -> Type['BaseHandlers']:
        """
        دریافت handler ایجادشده دینامیک بر اساس نام.

        پارامترها:
        - name: نام handler.

        خروجی:
        کلاس handler ایجادشده.
        """
        return create_handler(name, (BaseHandlers,), AUTHORIZED_HANDLERS)

# جایگزینی ماژول جاری با نمونه‌ای از Handlers
sys.modules[__name__] = Handlers(__name__)

# تعریف نوع‌های handler خاص
ChatUpdates: Type[BaseHandlers]
MessageUpdates: Type[BaseHandlers]
ShowActivities: Type[BaseHandlers]
ShowNotifications: Type[BaseHandlers]
RemoveNotifications: Type[BaseHandlers]