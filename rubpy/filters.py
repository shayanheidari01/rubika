import sys
import re
import warnings
from typing import Union, List, Pattern, Type, Any, Optional

# لیست عناصر عمومی برای export
__all__ = ['Operator', 'BaseModel', 'author_guids', 'object_guids', 'commands', 'regex',
           'AuthorGuids', 'ObjectGuids', 'Commands', 'RegexModel']

# لیست مدل‌های داخلی
__models__ = [
    'is_pinned', 'is_mute', 'count_unseen', 'message_id',
    'is_group', 'is_private', 'is_channel', 'is_in_contact',
    'text', 'original_update', 'object_guid', 'author_guid',
    'time', 'reply_message_id', 'is_me', 'is_forward', 'is_text',
    'music', 'file', 'photo', 'sticker', 'video', 'voice',
    'contact', 'location', 'poll', 'gif', 'is_event'
]

def create_model(
    name: str,
    base: tuple,
    authorize: List[str] = __models__,
    exception: bool = True,
    **kwargs
) -> Optional[Type['BaseModel']]:
    """
    ایجاد دینامیک یک مدل بر اساس نام و کلاس پایه.

    پارامترها:
    - name: نام مدل.
    - base: کلاس پایه برای مدل.
    - authorize: لیست نام‌های مدل‌های مجاز.
    - exception: آیا در صورت غیرمجاز بودن مدل خطا پرتاب شود.
    - kwargs: آرگومان‌های اضافی برای تنظیم کلاس.

    خروجی:
    کلاس مدل ایجادشده یا None در صورت غیرمجاز بودن.

    خطاها:
    - AttributeError: اگر مدل غیرمجاز باشد و exception=True.
    """
    if name in authorize:
        return type(name, base, {'__name__': name, **kwargs})
    
    if not exception:
        return None
    
    raise AttributeError(f"ماژول فاقد مدل با نام '{name}' است")

class Operator:
    """
    کلاس برای تعریف عملگرهای استفاده‌شده در فیلترهای مدل‌ها.
    """
    Or = 'OR'
    And = 'AND'
    Less = 'Less'
    Lesse = 'Lesse'
    Equal = 'Equal'
    Greater = 'Greater'
    Greatere = 'Greatere'
    Inequality = 'Inequality'

    def __init__(self, value: Any, operator: str):
        self.value = value
        self.operator = operator

    def __eq__(self, value: str) -> bool:
        return self.operator == value

class BaseModel:
    """
    کلاس پایه برای مدل‌های سفارشی.

    پارامترها:
    - func: تابع فیلتر (اختیاری).
    - filters: لیست یا تک فیلتر برای اعمال.
    - kwargs: آرگومان‌های اضافی.
    """
    def __init__(self, func: Optional[callable] = None, filters: Union[Any, List[Any]] = None, **kwargs) -> None:
        self.func = func
        self.filters = [filters] if filters and not isinstance(filters, list) else filters or []

    def insert(self, filter: 'Operator') -> 'BaseModel':
        """اضافه کردن فیلتر به لیست فیلترها."""
        self.filters.append(filter)
        return self

    def __or__(self, value: Any) -> 'BaseModel':
        return self.insert(Operator(value, Operator.Or))

    def __and__(self, value: Any) -> 'BaseModel':
        return self.insert( Operator(value, Operator.And))

    def __eq__(self, value: Any) -> bool:
        return self.insert(Operator(value, Operator.Equal))

    def __ne__(self, value: Any) -> bool:
        return self.insert(Operator(value, Operator.Inequality))

    def __lt__(self, value: Any) -> 'BaseModel':
        return self.insert(Operator(value, Operator.Less))

    def __le__(self, value: Any) -> 'BaseModel':
        return self.insert(Operator(value, Operator.Lesse))

    def __gt__(self, value: Any) -> 'BaseModel':
        return self.insert(Operator(value, Operator.Greater))

    def __ge__(self, value: Any) -> 'BaseModel':
        return self.insert(Operator(value, Operator.Greatere))

    async def build(self, update: Any) -> bool:
        """
        ساخت و اجرای فیلترها روی آپدیت.

        پارامترها:
        - update: شیء آپدیت برای بررسی.

        خروجی:
        True اگر فیلترها با موفقیت اعمال شوند، در غیر این صورت False.
        """
        result = getattr(update, self.__class__.__name__, None)
        
        if callable(self.func):
            result = await self.func(result) if update.is_async(self.func) else self.func(result)

        for filter in self.filters:
            value = filter.value
            if callable(value):
                value = await value(update, result) if update.is_async(value) else value(update, result)

            if self.func:
                value = await self.func(value) if update.is_async(self.func) else self.func(value)

            if filter == Operator.Or:
                result = result or value
            elif filter == Operator.And:
                result = result and value
            elif filter == Operator.Less:
                result = result < value
            elif filter == Operator.Lesse:
                result = result <= value
            elif filter == Operator.Equal:
                result = result == value
            elif filter == Operator.Greater:
                result = result > value
            elif filter == Operator.Greatere:
                result = result >= value
            elif filter == Operator.Inequality:
                result = result != value

        return bool(result)

    async def __call__(self, update: Any, *args, **kwargs) -> bool:
        """اجرای مدل روی آپدیت."""
        return await self.build(update)

class commands(BaseModel):
    """
    فیلتر برای دستورات در پیام‌های متنی.

    پارامترها:
    - commands: دستور یا لیست دستورات (رشته یا لیست رشته‌ها).
    - prefixes: پیشوند یا لیست پیشوندها (پیش‌فرض '/').
    - case_sensitive: حساسیت به حروف بزرگ و کوچک (پیش‌فرض False).
    """
    def __init__(
        self,
        commands: Union[str, List[str]],
        prefixes: Union[str, List[str]] = '/',
        case_sensitive: bool = False,
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.command_re = re.compile(r'([\"\'`])(.*?)(?<!\\)\1|(\S+)', re.UNICODE)
        self.commands = {c if case_sensitive else c.lower() for c in ([commands] if isinstance(commands, str) else commands)}
        self.prefixes = set([prefixes] if isinstance(prefixes, str) else prefixes or [''])
        self.case_sensitive = case_sensitive

    async def __call__(self, update: Any, *args, **kwargs) -> bool:
        """بررسی دستورات در متن آپدیت."""
        if not update.text:
            return False

        update['command'] = None
        for prefix in self.prefixes:
            if not update.text.startswith(prefix):
                continue

            without_prefix = update.text[len(prefix):]
            for cmd in self.commands:
                pattern = rf'^{cmd}(?:\s|$)' if self.case_sensitive else rf'^{cmd}(?:\s|$)' 
                if not re.match(pattern, without_prefix, flags=0 if self.case_sensitive else re.IGNORECASE):
                    continue

                without_command = re.sub(rf'{cmd}\s?', '', without_prefix, count=1, 
                                      flags=0 if self.case_sensitive else re.IGNORECASE)
                update['command'] = [cmd] + [
                    re.sub(r'\\([\"\'`])', r'\1', m.group(2) or m.group(3) or '')
                    for m in self.command_re.finditer(without_command)
                ]
                return True

        return False

class regex(BaseModel):
    """
    فیلتر برای تطبیق متن با عبارات منظم.

    پارامترها:
    - pattern: الگوی عبارت منظم.
    """
    def __init__(self, pattern: Union[str, Pattern], *args, **kwargs) -> None:
        self.pattern = re.compile(pattern) if isinstance(pattern, str) else pattern
        super().__init__(*args, **kwargs)

    async def __call__(self, update: Any, *args, **kwargs) -> bool:
        """تطبیق متن آپدیت با الگوی عبارت منظم."""
        if update.text is None:
            return False
        update.pattern_match = self.pattern.match(update.text)
        return bool(update.pattern_match)

class object_guids(BaseModel):
    """
    فیلتر بر اساس GUIDهای شیء.

    پارامترها:
    - args: GUID یا لیست/تاپل GUIDها.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.object_guids = []
        for arg in args:
            self.object_guids.extend(arg if isinstance(arg, (list, tuple)) else [arg])

    async def __call__(self, update: Any, *args, **kwargs) -> bool:
        """بررسی وجود GUID شیء در آپدیت."""
        return update.object_guid is not None and update.object_guid in self.object_guids

class author_guids(BaseModel):
    """
    فیلتر بر اساس GUIDهای نویسنده.

    پارامترها:
    - args: GUID یا لیست/تاپل GUIDها.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.author_guids = []
        for arg in args:
            self.author_guids.extend(arg if isinstance(arg, (list, tuple)) else [arg])

    async def __call__(self, update: Any, *args, **kwargs) -> bool:
        """بررسی وجود GUID نویسنده در آپدیت."""
        return update.author_guid is not None and update.author_guid in self.author_guids

class Models:
    """
    کلاس برای مدیریت و ایجاد مدل‌های خاص.
    """
    def __init__(self, name: str) -> None:
        self.__name__ = name

    def __eq__(self, value: object) -> bool:
        """بررسی برابری با کلاس پایه مدل‌ها."""
        return BaseModel in getattr(value, '__bases__', ())

    def __dir__(self) -> List[str]:
        """دریافت لیست مدل‌های مجاز."""
        return sorted(__models__)

    def __call__(self, name: str, *args, **kwargs) -> Type['BaseModel']:
        """فراخوانی مدل بر اساس نام."""
        return self.__getattr__(name)(*args, **kwargs)

    def __getattr__(self, name: str) -> Type['BaseModel']:
        """دریافت مدل دینامیک بر اساس نام."""
        if name in __all__:
            return globals()[name]
        return create_model(name, (BaseModel,), authorize=__models__, exception=False)

# جایگزینی ماژول جاری با نمونه‌ای از Models
sys.modules[__name__] = Models(__name__)

# تعریف نوع‌های مدل خاص
is_pinned: Type[BaseModel]
is_mute: Type[BaseModel]
count_unseen: Type[BaseModel]
message_id: Type[BaseModel]
is_group: Type[BaseModel]
is_private: Type[BaseModel]
is_channel: Type[BaseModel]
is_in_contact: Type[BaseModel]
text: Type[BaseModel]
original_update: Type[BaseModel]
object_guid: Type[BaseModel]
author_guid: Type[BaseModel]
time: Type[BaseModel]
reply_message_id: Type[BaseModel]
is_me: Type[BaseModel]
is_forward: Type[BaseModel]
is_event: Type[BaseModel]
is_text: Type[BaseModel]
music: Type[BaseModel]
file: Type[BaseModel]
photo: Type[BaseModel]
video: Type[BaseModel]
voice: Type[BaseModel]
contact: Type[BaseModel]
location: Type[BaseModel]
poll: Type[BaseModel]
gif: Type[BaseModel]
sticker: Type[BaseModel]
AuthorGuids, ObjectGuids, Commands, RegexModel = author_guids, object_guids, commands, regex