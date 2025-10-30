from typing import Optional, Union, Literal
import logging
import rubpy
from .sessions import SQLiteSession, StringSession
from .parser import Markdown
from .methods import Methods

class Client(Methods):
    """Main client for interacting with the Rubika API."""

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
        phone_number: Optional[str] = None,
        user_agent: Optional[str] = None,
        timeout: Union[str, int, float] = 20,
        lang_code: str = 'fa',
        parse_mode: Optional[Literal['html', 'markdown', 'mk']] = None,
        proxy: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        display_welcome: bool = False,
        platform: Literal['PWA', 'Android'] = 'PWA',
        max_retries: int = 5
    ) -> None:
        """
        Initialize the Rubika client.

        Parameters:
        - name: Session name or file path (str) or a StringSession instance.
        - auth: Authentication key (optional).
        - private_key: RSA private key (optional, str or bytes).
        - phone_number: Phone number (optional).
        - user_agent: User-Agent string (optional, defaults to Chrome).
        - timeout: Request timeout in seconds (default: 20).
        - lang_code: Language code (default: 'fa').
        - parse_mode: Message parsing mode ('html', 'markdown', 'mk', or None).
        - proxy: Proxy address (example: 'http://127.0.0.1:80').
        - logger: Logger instance for logging (optional).
        - display_welcome: Show welcome message (default: False).
        - platform: Client platform ('PWA' or 'Android').
        - max_retries: Maximum number of retries for requests (default: 5).

        Raises:
        - ValueError: If any input is invalid.
        - TypeError: If the 'name' parameter is not str or StringSession.
        """
        super().__init__()

        # Configure platform
        self.DEFAULT_PLATFORM = self.DEFAULT_PLATFORM.copy()
        if platform.lower() == 'android':
            self.DEFAULT_PLATFORM['platform'] = 'Android'

        # Validate inputs
        if auth and not isinstance(auth, str):
            raise ValueError("The 'auth' parameter must be a string.")
        if phone_number and not isinstance(phone_number, str):
            raise ValueError("The 'phone_number' parameter must be a string.")
        if user_agent and not isinstance(user_agent, str):
            raise ValueError("The 'user_agent' parameter must be a string.")
        if not isinstance(timeout, (int, float)):
            try:
                timeout = float(timeout)
            except (ValueError, TypeError):
                raise ValueError("The 'timeout' parameter must be a number.")

        # Setup session
        if isinstance(name, str):
            session = SQLiteSession(name)
        elif isinstance(name, StringSession):
            session = name
        else:
            raise TypeError("The 'name' parameter must be a string or StringSession instance.")

        # Configure parse_mode
        valid_parse_modes = {'html', 'markdown', 'mk'}
        if parse_mode is not None:
            parse_mode = parse_mode.lower()
            if parse_mode not in valid_parse_modes:
                raise ValueError(f"The 'parse_mode' parameter must be one of {valid_parse_modes} or None.")
        else:
            parse_mode = 'markdown'

        # Configure logger
        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(__name__)

        # Format private key if necessary
        if isinstance(private_key, str):
            if not private_key.startswith('-----BEGIN RSA PRIVATE KEY-----'):
                private_key = f'-----BEGIN RSA PRIVATE KEY-----\n{private_key}'
            if not private_key.endswith('\n-----END RSA PRIVATE KEY-----'):
                private_key += '\n-----END RSA PRIVATE KEY-----'

        # Assign variables
        self.name = name
        self.auth = auth
        self.logger = logger
        self.private_key = private_key
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

        # Welcome message (optional)
        if display_welcome:
            self.logger.info("Rubika client initialized successfully.")

    def __enter__(self) -> "Client":
        """Support for context manager to start the client."""
        return self.start()

    def __exit__(self, *args, **kwargs) -> None:
        """Support for context manager to disconnect the client."""
        try:
            self.disconnect()
        except Exception as e:
            self.logger.warning(f"Error while disconnecting: {e}")

    async def __aenter__(self) -> "Client":
        """Support for async context manager to start the client."""
        return await self.start()

    async def __aexit__(self, *args, **kwargs) -> None:
        """Support for async context manager to disconnect the client."""
        try:
            await self.disconnect()
        except Exception as e:
            self.logger.warning(f"Error while disconnecting: {e}")

    async def stop(self) -> None:
        if self.connection.session.closed:
            return
        await self.disconnect()