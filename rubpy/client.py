from typing import Optional, Union, Literal
import logging
import rubpy
from .sessions import SQLiteSession, StringSession
from .parser import Markdown
from .methods import Methods

class Client(Methods):
    """کلاینت اصلی برای تعامل با API روبیکا."""

    DEFAULT_PLATFORM = {
        'app_name': 'Main',
        'app_version': '2.4.6',
        'platform': 'PWA',
        'package': 'm.rubika.ir',
    }

    USER_AGENT = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/102.0.0.0 Safari/537.36'
    )

    API_VERSION = '6'

    def __init__(
        self,
        name: Union[str, StringSession],
        auth: Optional[str] = None,
        private_key: Optional[Union[str, bytes]] = None,
        bot_token: Optional[str] = None,
        phone_number: Optional[str] = None,
        user_agent: Optional[str] = None,
        timeout: Union[str, int, float] = 20,
        lang_code: str = 'fa',
        parse_mode: Optional[Literal['html', 'markdown', 'mk']] = None,
        proxy: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        display_welcome: bool = False,
        platform: Literal['Web', 'Android'] = 'Web',
        max_retries: int = 5
    ) -> None:
        """
        مقداردهی اولیه کلاینت روبیکا.

        پارامترها:
        - name: نام یا مسیر فایل سشن (str) یا نمونه StringSession.
        - auth: کلید احراز هویت (اختیاری).
        - private_key: کلید خصوصی RSA (اختیاری، رشته یا بایت).
        - bot_token: توکن ربات (اختیاری).
        - phone_number: شماره تلفن (اختیاری).
        - user_agent: رشته User-Agent (اختیاری، پیش‌فرض مرورگر کروم).
        - timeout: زمان انتظار درخواست‌ها (ثانیه، پیش‌فرض 20).
        - lang_code: کد زبان (پیش‌فرض 'fa').
        - parse_mode: حالت تجزیه پیام (html، markdown، mk یا None).
        - proxy: آدرس پروکسی (مثال: 'http://127.0.0.1:80').
        - logger: شیء Logger برای لاگ‌گیری (اختیاری).
        - display_welcome: نمایش پیام خوش‌آمدگویی (پیش‌فرض False).
        - platform: پلتفرم کلاینت ('Web' یا 'Android').

        خطاها:
        - ValueError: در صورت نامعتبر بودن ورودی‌ها.
        - TypeError: در صورت نادرست بودن نوع name.
        """
        super().__init__()

        # تنظیم پلتفرم
        self.DEFAULT_PLATFORM = self.DEFAULT_PLATFORM.copy()
        if platform.lower() == 'android':
            self.DEFAULT_PLATFORM['platform'] = 'Android'

        # اعتبارسنجی ورودی‌ها
        if auth and not isinstance(auth, str):
            raise ValueError('پارامتر auth باید رشته باشد.')
        if bot_token and not isinstance(bot_token, str):
            raise ValueError('پارامتر bot_token باید رشته باشد.')
        if phone_number and not isinstance(phone_number, str):
            raise ValueError('پارامتر phone_number باید رشته باشد.')
        if user_agent and not isinstance(user_agent, str):
            raise ValueError('پارامتر user_agent باید رشته باشد.')
        if not isinstance(timeout, (int, float)):
            try:
                timeout = float(timeout)
            except (ValueError, TypeError):
                raise ValueError('پارامتر timeout باید عدد باشد.')

        # تنظیم سشن
        if isinstance(name, str):
            session = SQLiteSession(name)
        elif isinstance(name, StringSession):
            session = name
        else:
            raise TypeError('پارامتر name باید رشته یا نمونه StringSession باشد.')

        # تنظیم parse_mode
        valid_parse_modes = {'html', 'markdown', 'mk'}
        if parse_mode is not None:
            parse_mode = parse_mode.lower()
            if parse_mode not in valid_parse_modes:
                raise ValueError(f'پارامتر parse_mode باید یکی از {valid_parse_modes} یا None باشد.')
        else:
            parse_mode = 'markdown'

        # تنظیم logger
        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(__name__)

        # تنظیم کلید خصوصی
        if isinstance(private_key, str):
            if not private_key.startswith('-----BEGIN RSA PRIVATE KEY-----'):
                private_key = f'-----BEGIN RSA PRIVATE KEY-----\n{private_key}'
            if not private_key.endswith('\n-----END RSA PRIVATE KEY-----'):
                private_key += '\n-----END RSA PRIVATE KEY-----'

        # مقداردهی متغیرها
        self.name = name
        self.auth = auth
        self.logger = logger
        self.private_key = private_key
        self.bot_token = bot_token
        self.phone_number = phone_number
        self.display_welcome = display_welcome
        self.user_agent = user_agent or self.USER_AGENT
        self.lang_code = lang_code
        self.timeout = timeout
        self.session = session
        self.parse_mode = parse_mode
        self.proxy = proxy
        self.markdown = Markdown()
        self.database = None
        self.decode_auth = None
        self.import_key = None
        self.is_sync = False
        self.guid = None
        self.key = None
        self.handlers = {}
        self.DEFAULT_PLATFORM['lang_code'] = lang_code
        self.max_retries = max_retries

        # حذف پیام خوش‌آمدگویی برای بهینه‌سازی
        if display_welcome:
            self.logger.info("کلاینت روبیکا با موفقیت مقداردهی شد.")

    def __enter__(self) -> "Client":
        """پشتیبانی از context manager برای شروع کلاینت."""
        return self.start()

    def __exit__(self, *args, **kwargs) -> None:
        """پشتیبانی از context manager برای قطع اتصال."""
        try:
            self.disconnect()
        except Exception as e:
            self.logger.warning(f"خطا در قطع اتصال: {e}")

    async def __aenter__(self) -> "Client":
        """پشتیبانی از async context manager برای شروع کلاینت."""
        return await self.start()

    async def __aexit__(self, *args, **kwargs) -> None:
        """پشتیبانی از async context manager برای قطع اتصال."""
        try:
            await self.disconnect()
        except Exception as e:
            self.logger.warning(f"خطا در قطع اتصال: {e}")