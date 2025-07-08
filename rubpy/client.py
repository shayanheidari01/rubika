from .sessions import SQLiteSession, StringSession
from .parser import Markdown
from .methods import Methods
from typing import Optional, Union
from . import __name__ as logger_name
import logging


class Client(Methods):
    DEFAULT_PLATFORM = {
        'app_name': 'Main',
        'app_version': '4.4.6',
        'platform': 'Web',
        'package': 'web.rubika.ir',
        }

    USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/102.0.0.0 Safari/537.36')

    API_VERSION = '6'

    def __init__(self,
                 name: str,
                 auth: Optional[str] = None,
                 private_key: Optional[Union[str, bytes]] = None,
                 bot_token: Optional[str] = None,
                 phone_number: Optional[str] = None,
                 user_agent: Optional[str] = None or USER_AGENT,
                 timeout: Optional[Union[str, int]] = 20,
                 lang_code: Optional[str] = 'fa',
                 parse_mode: Optional[str] = None,
                 proxy: str = None,
                 logger: "logging.Logger" = None,
                 display_welcome: bool = True,
    ) -> None:
        """Client
            Args:
                name (`str` | `rubpy.sessions.StringSession`):
                    The file name of the session file that is used
                    if there is a string Given (may be a complete path)
                    or it could be a string session
                    [rubpy.sessions.StringSession]
                
                auth (`str`, optional): To set up auth
                private_key (`str`, optional): To set up private key
                bot_token (`str`, optional): To set up bot token
                phone_number (`str`, optional): To set up phone number

                proxy (`str`, optional):
                    To set up a proxy, example:
                        proxy='http://127.0.0.1:80'

                parse_mode (`bool`, optional):
                    To set the parse mode `` default( `None` ) ``

                user_agent (`str`, optional):
                    Client uses the web version, You can set the usr-user_agent

                timeout (`int` | `float`, optional):
                    To set the timeout `` default( `20 seconds` )``

                logger (`logging.Logger`, optional):
                    Logger base for use.

                lang_code(`str`, optional):
                    To set the lang_code `` default( `fa` ) ``

                display_welcome (`bool`, optional):
                    To set the display welcome `` default( `True` ) ``
        """
        super().__init__()

        if auth and not isinstance(auth, str):
            raise ValueError('`auth` is `string` arg.')

        if isinstance(private_key, str):
            if not private_key.startswith('-----BEGIN RSA PRIVATE KEY-----'):
                private_key = ''.join(['-----BEGIN RSA PRIVATE KEY-----\n', private_key.strip(), '\n-----END RSA PRIVATE KEY-----'])

        if bot_token and not isinstance(bot_token, str):
            raise ValueError('`bot_token` is `string` arg.')

        if phone_number and not isinstance(phone_number, str):
            raise ValueError('`phone_number` is `string` arg.')

        if user_agent and not isinstance(user_agent, str):
            raise ValueError('`user_agent` is `string` arg.')

        if not isinstance(timeout, int):
            timeout = int(timeout)

        if isinstance(name, str):
            session = SQLiteSession(name)

        elif not isinstance(name, StringSession):
            raise TypeError('The given session must be a '
                            'str or [rubpy.sessions.StringSession]')

        if parse_mode not in (None, 'html', 'markdown', 'mk'):
            raise ValueError('The `parse_mode` argument can only be in `("html", "markdown", "mk")`.')

        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger_name)
    
        self.DEFAULT_PLATFORM['lang_code'] = lang_code
        self.name = name
        self.auth = auth
        self.logger = logger
        self.private_key = private_key
        self.bot_token = bot_token
        self.phone_number = phone_number
        self.display_welcome = display_welcome
        self.user_agent = user_agent
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

    def __enter__(self) -> "Client":
        return self.start()

    def __exit__(self, *args, **kwargs):
        try:
            return self.disconnect()

        except Exception:
            pass

    async def __aenter__(self):
        return await self.start()

    async def __aexit__(self, *args, **kwargs):
        try:
            return await self.disconnect()

        except Exception:
            pass