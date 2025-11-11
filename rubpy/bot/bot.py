"""Client utilities for interacting with the Rubika bot API."""

import asyncio
import dataclasses
import inspect
import mimetypes
from pathlib import Path
import aiohttp
from aiohttp import web
from aiohttp.client_exceptions import (
    ClientError,
    ClientResponseError,
    ContentTypeError,
)
import json
from typing import Any, Callable, Dict, List, Literal, Optional, Union, Tuple
import logging
from collections import deque
import time
import uuid

from rubpy.parser.markdown import Markdown
from rubpy.bot.enums import ChatKeypadTypeEnum, UpdateTypeEnum
from rubpy.bot.filters import Filter
from rubpy.bot.models import (
    Keypad,
    InlineMessage,
    Metadata,
    Update,
    Message,
    MessageId,
    Chat,
    Bot,
)
from rubpy.bot.exceptions import APIException
from rubpy.enums import ParseMode

# Setup logging
# logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def has_time_passed(last_time, seconds: int = 5) -> bool:
    """
    Check if a certain amount of time has passed since the last time.

    Args:
        last_time: The last time in seconds.
        seconds: The amount of time to check for.

    Returns:
        bool: True if the time has passed, False otherwise.
    """
    try:
        timestamp = int(float(last_time))
        now = time.time()
        return (now - timestamp) > seconds
    except (TypeError, ValueError):
        return False


class BotClient:
    """
    Asynchronous client for managing Rubika bot interactions.

    Attributes:
        token: Bot authentication token provided by Rubika.
        base_url: The base URL for API requests.
        handlers: A dictionary of registered handlers.
        start_handlers: A list of registered startup handlers.
        shutdown_handlers: A list of registered shutdown handlers.
        middlewares: A list of registered middleware functions.
        session: The active aiohttp session.
        running: A flag indicating whether the client is running.
        next_offset_id: The next offset ID for API requests.
        processed_messages: A deque of processed messages.
        rate_limit: The minimum delay in seconds between API requests.
        last_request_time: The last time an API request was made.
        first_get_updates: A flag indicating whether this is the first get updates request.
        use_webhook: A flag indicating whether the client should operate in webhook mode.
        timeout: The overall timeout for API requests.
        connector: An optional shared aiohttp connector instance.
        max_retries: The maximum number of retries for retryable responses.
        backoff_factor: The base delay in seconds for exponential backoff.
        retry_statuses: A set of HTTP status codes that should trigger retries.
    """

    BASE_URL = "https://botapi.rubika.ir/v3/{}/"

    def __init__(
        self,
        token: str,
        rate_limit: float = 0.5,
        use_webhook: bool = False,
        timeout: Union[int, float] = 10.0,
        connector: "aiohttp.TCPConnector" = None,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        retry_statuses: Optional[Tuple[int, ...]] = None,
        poll_interval: float = 0.5,
        long_poll_timeout: float = 30.0,
        parse_mode: Optional[Union[ParseMode, str]] = ParseMode.MARKDOWN,
    ) -> None:
        """
        Initialize a new :class:`BotClient` instance.

        Args:
            token: Bot authentication token provided by Rubika.
            rate_limit: Minimum delay in seconds between API requests.
            use_webhook: Whether the client should operate in webhook mode.
            timeout: Overall timeout for API requests.
            connector: Optional shared aiohttp connector instance.
            max_retries: Maximum number of retries for retryable responses.
            backoff_factor: Base delay (in seconds) for exponential backoff.
            retry_statuses: HTTP status codes that should trigger retries.
        """

        self.token = token
        self.base_url = self.BASE_URL.format(token)
        self.handlers: Dict[str, List[Tuple[Tuple[Filter, ...], Callable]]] = {}
        self.start_handlers: list[Callable] = []
        self.shutdown_handlers: list[Callable] = []
        self.middlewares: list[Callable] = []
        self.session = None
        self.running = False
        self.next_offset_id = None
        self.processed_messages = deque(maxlen=500)
        self._markdown = Markdown()
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.first_get_updates = True
        self.use_webhook = use_webhook
        self.timeout = timeout
        self.connector = connector
        self.max_retries = max(1, int(max_retries))
        self.backoff_factor = max(0.0, float(backoff_factor))
        self.retry_statuses = set(retry_statuses or (408, 425, 429, 500, 502, 503, 504))
        self._session_lock = asyncio.Lock()
        self.poll_interval = max(0.1, float(poll_interval))
        self.long_poll_timeout = max(self.poll_interval, float(long_poll_timeout))
        logger.info(
            "Rubika client initialized (use_webhook=%s, rate_limit=%.2fs)",
            use_webhook,
            rate_limit,
        )
        self.parse_mode = self._normalize_parse_mode(parse_mode)

    @staticmethod
    def _normalize_parse_mode(
        parse_mode: Optional[Union[ParseMode, str]]
    ) -> Optional[ParseMode]:
        if parse_mode is None:
            return None
        if isinstance(parse_mode, ParseMode):
            return parse_mode
        if isinstance(parse_mode, str):
            value = parse_mode.strip()
            if not value:
                return None
            try:
                return ParseMode(value.lower())
            except ValueError as exc:  # pragma: no cover - defensive
                allowed = ", ".join(mode.value for mode in ParseMode)
                raise ValueError(
                    f"Unsupported parse_mode {parse_mode!r}. Expected one of: {allowed}"
                ) from exc
        raise TypeError(
            "parse_mode must be an instance of ParseMode, a string, or None"
        )

    def _resolve_parse_mode(
        self, parse_mode: Optional[Union[ParseMode, str]]
    ) -> Optional[ParseMode]:
        return (
            self._normalize_parse_mode(parse_mode)
            if parse_mode is not None
            else self.parse_mode
        )

    def _apply_text_formatting(
        self,
        payload: Dict[str, Any],
        text: Optional[str],
        parse_mode: Optional[Union[ParseMode, str]],
        metadata: Optional[Metadata] = None,
    ) -> Optional[ParseMode]:
        """
        Apply text formatting (parse_mode) and metadata to the payload.
        
        Args:
            payload: The request payload dictionary to update.
            text: The text content to format.
            parse_mode: The parse mode to use (Markdown, HTML, or None).
            metadata: Optional metadata to include in the payload.
            
        Returns:
            The resolved parse mode that was applied.
        """
        resolved_parse_mode = self._resolve_parse_mode(parse_mode)
        
        # Apply parse mode formatting
        if isinstance(text, str):
            if resolved_parse_mode is ParseMode.MARKDOWN:
                payload.update(self._markdown.to_metadata(text))
            elif resolved_parse_mode is ParseMode.HTML:
                markdown_text = self._markdown.to_markdown(text)
                payload.update(self._markdown.to_metadata(markdown_text))
        
        # Apply metadata if provided
        if isinstance(metadata, Metadata):
            payload["metadata"] = dataclasses.asdict(metadata)
            
        return resolved_parse_mode
    
    def _apply_text_parse_mode(
        self,
        payload: Dict[str, Any],
        text: Optional[str],
        parse_mode: Optional[Union[ParseMode, str]],
    ) -> Optional[ParseMode]:
        """Deprecated: Use _apply_text_formatting instead."""
        return self._apply_text_formatting(payload, text, parse_mode, None)

    def on_start(self):
        """
        Decorator to register startup handlers.

        Example:
            @bot.on_start()
            async def hello(bot):
                print("Bot started!")
        """
        def decorator(func: Callable):
            self.start_handlers.append(func)
            return func
        return decorator

    async def __aenter__(self) -> "BotClient":
        """Asynchronous context manager entry point."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        """Ensure the client stops when leaving an async context."""
        await self.stop()

    def __enter__(self) -> "BotClient":
        """Synchronous context manager entry point."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Ensure the client stops when leaving a sync context."""
        self.stop()

    async def _rate_limit_delay(self):
        """
        Enforce the rate limit by waiting for a certain amount of time.

        This method checks the time elapsed since the last request and waits
        for the remaining time if necessary.
        """
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            await asyncio.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()

    async def start(self):
        """Start the client session and execute registered startup hooks."""
        await self._ensure_session()
        self.running = True

        for handler in self.start_handlers:
            if inspect.iscoroutinefunction(handler):
                await handler(self)
            else:
                handler(self)

        logger.info("RubikaPY bot client started")

    async def stop(self):
        """Stop the client and run shutdown hooks."""
        await self._close_session()
        self.running = False

        for handler in self.shutdown_handlers:
            if inspect.iscoroutinefunction(handler):
                await handler(self)
            else:
                handler(self)

        logger.info("RubikaPY bot client stopped")
    
    def on_shutdown(self):
        """
        Decorator to register shutdown handlers.
        
        Example:
            @bot.on_shutdown()
            async def bye(bot):
                print("Bot stopped!")
        """
        def decorator(func: Callable):
            self.shutdown_handlers.append(func)
            return func
        return decorator
    
    def middleware(self):
        """
        Decorator to register a middleware function.

        Middleware receives (bot, update, next_middleware).
        It must call `await next_middleware()` to continue chain.

        Example:
            @bot.middleware()
            async def logger(bot, update, call_next):
                print("🔹 Update received:", update)
                await call_next()
        """
        def decorator(func: Callable):
            self.middlewares.append(func)
            logger.info("Middleware %s registered", func.__name__)
            return func
        return decorator

    async def _make_request(
        self, method: str, data: Dict, *, extra_timeout: Optional[float] = None
    ) -> Dict:
        """Perform an API request with retry and response validation."""
        await self._rate_limit_delay()
        url = f"{self.base_url}{method}"

        last_error: Optional[BaseException] = None

        for attempt in range(1, self.max_retries + 1):
            try:
                await self._ensure_session()
                if not self.session:
                    raise RuntimeError("Client session is not initialized")

                timeout = None
                if extra_timeout is not None:
                    total_timeout = self.timeout + max(0.0, float(extra_timeout))
                    timeout = aiohttp.ClientTimeout(total=total_timeout)

                async with self.session.post(url, json=data, timeout=timeout) as response:
                    try:
                        response.raise_for_status()
                    except ClientResponseError as exc:
                        body = await response.text()
                        if self._is_retryable_status(exc.status) and attempt < self.max_retries:
                            last_error = exc
                            logger.warning(
                                "Retryable HTTP error %s on %s attempt %s: %s",
                                exc.status,
                                method,
                                attempt,
                                body,
                            )
                            await self._sleep_backoff(attempt)
                            continue
                        raise APIException(status=str(exc.status), dev_message=body or exc.message)

                    try:
                        result = await response.json(content_type=None)
                    except ContentTypeError:
                        text = await response.text()
                        raise APIException(status="InvalidResponse", dev_message=text)

                    logger.debug(
                        "API response for %s returned status=%s",
                        method,
                        result.get("status"),
                    )

                    if result.get("status") != "OK":
                        raise APIException(
                            status=result.get("status", "ERROR"),
                            dev_message=result.get("dev_message"),
                        )

                    return result["data"]

            except (ClientError, asyncio.TimeoutError) as exc:
                last_error = exc
                if attempt >= self.max_retries:
                    break
                logger.warning(
                    "Network error on %s attempt %s: %s", method, attempt, str(exc)
                )
                await self._sleep_backoff(attempt)

        if last_error:
            raise last_error

        raise APIException(status="UnknownError", dev_message=f"Failed to call {method}")

    async def _ensure_session(self) -> None:
        """Ensure there is an open aiohttp session available for use."""
        if self.session and not self.session.closed:
            return

        async with self._session_lock:
            if self.session and not self.session.closed:
                return

            timeout = aiohttp.ClientTimeout(total=self.timeout)
            connector = self.connector or aiohttp.TCPConnector(
                limit=50,
                limit_per_host=10,
                ttl_dns_cache=300,
                enable_cleanup_closed=True,
            )
            connector_owner = self.connector is None
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
                connector_owner=connector_owner,
                headers={"user-agent": "rubpy-7.1.32"}
            )

    async def _close_session(self) -> None:
        """Close the active aiohttp session if it exists."""
        if self.session and not self.session.closed:
            await self.session.close()
        self.session = None

    def _is_retryable_status(self, status: Optional[int]) -> bool:
        return status in self.retry_statuses if status is not None else False

    async def _sleep_backoff(self, attempt: int) -> None:
        """Wait for an exponentially increasing delay between retries."""
        if self.backoff_factor <= 0:
            return
        delay = self.backoff_factor * (2 ** (attempt - 1))
        await asyncio.sleep(delay)

    async def get_me(self) -> Bot:
        result = await self._make_request("getMe", {})
        return Bot(**result["bot"])

    async def send_message(
        self,
        chat_id: str,
        text: str,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ) -> MessageId:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "disable_notification": disable_notification,
            "chat_keypad_type": chat_keypad_type.value,
        }

        if chat_keypad:
            payload["chat_keypad"] = dataclasses.asdict(chat_keypad)
        if inline_keypad:
            payload["inline_keypad"] = dataclasses.asdict(inline_keypad)
        if reply_to_message_id:
            payload["reply_to_message_id"] = str(reply_to_message_id)
        if text:
            self._apply_text_formatting(payload, text, parse_mode, metadata)

        result = await self._make_request("sendMessage", payload)
        result["chat_id"] = chat_id
        result["client"] = self
        return MessageId(**result)

    async def send_sticker(
        self,
        chat_id: str,
        sticker_id: str,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE,
    ) -> MessageId:
        payload = {
            "chat_id": chat_id,
            "sticker_id": sticker_id,
            "disable_notification": disable_notification,
            "chat_keypad_type": chat_keypad_type.value,
        }
        if chat_keypad:
            payload["chat_keypad"] = dataclasses.asdict(chat_keypad)
        if inline_keypad:
            payload["inline_keypad"] = dataclasses.asdict(inline_keypad)
        if reply_to_message_id:
            payload["reply_to_message_id"] = str(reply_to_message_id)

        result = await self._make_request("sendSticker", payload)
        result["chat_id"] = chat_id
        result["client"] = self
        return MessageId(**result)

    async def send_file(
        self,
        chat_id: str,
        file: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        file_name: Optional[str] = None,
        type: Literal["File", "Image", "Voice", "Music", "Gif", "Video"] = "File",
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ) -> MessageId:
        if file:
            file_name = file_name or Path(file).name
            upload_url = await self.request_send_file(type)
            file_id = await self.upload_file(upload_url, file_name, file)

        payload = {
            "chat_id": chat_id,
            "file_id": file_id,
            "text": text,
            "disable_notification": disable_notification,
            "chat_keypad_type": chat_keypad_type.value,
        }
        if chat_keypad:
            payload["chat_keypad"] = dataclasses.asdict(chat_keypad)
        if inline_keypad:
            payload["inline_keypad"] = dataclasses.asdict(inline_keypad)
        if reply_to_message_id:
            payload["reply_to_message_id"] = str(reply_to_message_id)
        self._apply_text_formatting(payload, text, parse_mode, metadata)
        
        result = await self._make_request("sendFile", payload)
        result["chat_id"] = chat_id
        result["client"] = self
        result["file_id"] = file_id
        return MessageId(**result)
    
    async def send_music(
        self,
        chat_id: str,
        file: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        file_name: Optional[str] = None,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ) -> MessageId:
        if file:
            file_name = file_name or Path(file).name
            upload_url = await self.request_send_file("File")
            file_id = await self.upload_file(upload_url, file_name[:-4] + ".ogg", file)

        payload = {
            "chat_id": chat_id,
            "file_id": file_id,
            "text": text,
            "disable_notification": disable_notification,
            "chat_keypad_type": chat_keypad_type.value,
        }
        if chat_keypad:
            payload["chat_keypad"] = dataclasses.asdict(chat_keypad)
        if inline_keypad:
            payload["inline_keypad"] = dataclasses.asdict(inline_keypad)
        if reply_to_message_id:
            payload["reply_to_message_id"] = str(reply_to_message_id)
        if text:
            self._apply_text_formatting(payload, text, parse_mode, metadata)

        result = await self._make_request("sendFile", payload)
        result["chat_id"] = chat_id
        result["client"] = self
        result["file_id"] = file_id
        return MessageId(**result)

    async def send_voice(
        self,
        chat_id: str,
        file: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        file_name: Optional[str] = None,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ) -> MessageId:
        if file:
            file_name = file_name or Path(file).name
            upload_url = await self.request_send_file("File")
            file_id = await self.upload_file(upload_url, file_name[:-4] + ".ogg", file)

        payload = {
            "chat_id": chat_id,
            "file_id": file_id,
            "text": text,
            "disable_notification": disable_notification,
            "chat_keypad_type": chat_keypad_type.value,
        }
        if chat_keypad:
            payload["chat_keypad"] = dataclasses.asdict(chat_keypad)
        if inline_keypad:
            payload["inline_keypad"] = dataclasses.asdict(inline_keypad)
        if reply_to_message_id:
            payload["reply_to_message_id"] = str(reply_to_message_id)
        if text:
            self._apply_text_formatting(payload, text, parse_mode, metadata)

        result = await self._make_request("sendFile", payload)
        result["chat_id"] = chat_id
        result["client"] = self
        result["file_id"] = file_id
        return MessageId(**result)

    async def request_send_file(
        self, type: Literal["File", "Image", "Voice", "Music", "Gif", "Video"]
    ) -> str:
        if type not in ["File", "Image", "Voice", "Music", "Gif", "Video"]:
            raise ValueError(
                "type is just be in ['File', 'Image', 'Voice', 'Music', 'Gif', 'Video']"
            )

        result = await self._make_request("requestSendFile", {"type": type})
        return result["upload_url"]

    async def upload_file(self, url: str, file_name: str, file_path: str) -> str:
        form = aiohttp.FormData()
        form.add_field(
            name="file",
            value=open(file_path, "rb"),
            filename=file_name,
            content_type="application/octet-stream",  # Replace if the real MIME type is known.
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=form, ssl=False) as res:
                if res.status != 200:
                    text = await res.text()
                    raise aiohttp.ClientResponseError(
                        res.request_info, res.history, status=res.status, message=text
                    )

                data = await res.json()
                return data["data"]["file_id"]  # Ensure this matches the upstream JSON shape.

    async def get_file(self, file_id: str) -> str:
        result = await self._make_request("getFile", {"file_id": file_id})
        return result["download_url"]

    async def send_poll(
        self,
        chat_id: str,
        question: str,
        options: List[str],
        type: Literal["Regular", "Quiz"] = "Regular",
        allows_multiple_answers: bool = False,
        is_anonymous: bool = True,
        correct_option_index: Optional[int] = None,
        explanation: Optional[str] = None,
        reply_to_message_id: Optional[str] = None,
        disable_notification: bool = False,
        chat_keypad: Optional[Keypad] = None,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE,

    ) -> MessageId:
        result = await self._make_request(
            "sendPoll", {
                "chat_id": chat_id,
                "question": question,
                "options": options,
                "type": type,
                "allows_multiple_answers": allows_multiple_answers,
                "is_anonymous": is_anonymous,
                "correct_option_index": correct_option_index,
                "explanation": explanation,
                "reply_to_message_id": reply_to_message_id,
                "disable_notification": disable_notification,
                "chat_keypad": dataclasses.asdict(chat_keypad),
                "chat_keypad_type": chat_keypad_type.value,
            }
        )
        result["chat_id"] = chat_id
        result["client"] = self
        return MessageId(**result)

    async def send_location(
        self,
        chat_id: str,
        latitude: Union[str, float],
        longitude: Union[str, float],
        chat_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE,
    ) -> MessageId:
        payload = {
            "chat_id": chat_id,
            "latitude": str(latitude),
            "longitude": str(longitude),
            "disable_notification": disable_notification,
            "chat_keypad_type": chat_keypad_type.value,
        }
        if chat_keypad:
            payload["chat_keypad"] = dataclasses.asdict(chat_keypad)
        if reply_to_message_id:
            payload["reply_to_message_id"] = str(reply_to_message_id)
        result = await self._make_request("sendLocation", payload)
        result["chat_id"] = chat_id
        result["client"] = self
        return MessageId(**result)

    async def send_contact(
        self,
        chat_id: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        chat_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE,
    ) -> MessageId:
        payload = {
            "chat_id": chat_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "disable_notification": disable_notification,
            "chat_keypad_type": chat_keypad_type.value,
        }

        if chat_keypad:
            payload["chat_keypad"] = dataclasses.asdict(chat_keypad)
        if reply_to_message_id:
            payload["reply_to_message_id"] = str(reply_to_message_id)

        result = await self._make_request("sendContact", payload)
        result["chat_id"] = chat_id
        result["client"] = self
        return MessageId(**result)

    async def get_updates(
        self, limit: int = 100, offset_id: str = ""
    ) -> List[Update]:
        """
        Fetch updates from the server.

        Args:
            limit (int): Maximum number of updates to fetch.
            offset_id (str): Offset for pagination.

        Returns:
            List[Update]: Parsed updates as Update objects.
        """
        # Build payload inline to avoid redundant conditionals.
        data = {"limit": limit, **({"offset_id": offset_id} if offset_id else {})}

        response = await self._make_request("getUpdates", data)
        updates_raw = response.get("updates")
        if not updates_raw:
            return []

        # Use list comprehension to parse updates efficiently.
        return [
            Update(
                type=u.get("type", ""),
                chat_id=u.get("chat_id", ""),
                client=self,
                removed_message_id=str(u.get("removed_message_id", "")),
            )
            for u in updates_raw
        ]

    async def updater(
        self,
        limit: int = 100,
        offset_id: str = "",
        poll_timeout: Optional[float] = None,
    ) -> List[Union[Update, InlineMessage]]:
        data = {"limit": limit}
        updates = []
        if offset_id or self.next_offset_id:
            data["offset_id"] = self.next_offset_id if not offset_id else offset_id

        if poll_timeout:
            timeout_seconds = max(1, int(poll_timeout))
            data["timeout"] = timeout_seconds

        try:
            response = await self._make_request(
                "getUpdates",
                data,
                extra_timeout=poll_timeout if poll_timeout else None,
            )
            self.next_offset_id = response.get("next_offset_id", self.next_offset_id)
            for item in response.get("updates", []):
                update = self._parse_update(item)
                if update:
                    if update.type == UpdateTypeEnum.RemovedMessage:
                        continue

                    last_time = (
                        getattr(update, "new_message", None) and update.new_message.time
                    ) or (
                        getattr(update, "updated_message", None)
                        and round(time.time())
                    )

                    # Skip stale updates older than the configured threshold.
                    if has_time_passed(last_time, 5):
                        continue

                    updates.append(update)

        except Exception as e:
            logger.exception("Failed to get updates: %s", e)

        if self.first_get_updates:
            self.first_get_updates = False
            return []

        return updates

    async def get_chat(self, chat_id: str) -> Chat:
        result = await self._make_request("getChat", {"chat_id": chat_id})
        return Chat(**result["chat"])

    async def forward_message(
        self,
        from_chat_id: str,
        message_id: str,
        to_chat_id: str,
        disable_notification: bool = False,
    ) -> MessageId:
        result = await self._make_request(
            "forwardMessage",
            {
                "from_chat_id": from_chat_id,
                "message_id": str(message_id),
                "to_chat_id": to_chat_id,
                "disable_notification": disable_notification,
            },
        )
        result["chat_id"] = to_chat_id
        result["client"] = self
        return MessageId(**result)

    async def edit_message_text(
        self,
        chat_id: str,
        message_id: str,
        text: str,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ) -> bool:
        payload = {
            "chat_id": chat_id,
            "message_id": str(message_id),
            "text": text,
        }
        self._apply_text_formatting(payload, text, parse_mode, metadata)

        result = await self._make_request(
            "editMessageText",
            payload,
        )
        return not bool(result)

    async def edit_message_keypad(
        self, chat_id: str, message_id: str, inline_keypad: Keypad
    ) -> bool:
        result = await self._make_request(
            "editMessageKeypad",
            {
                "chat_id": chat_id,
                "message_id": str(message_id),
                "inline_keypad": dataclasses.asdict(inline_keypad),
            },
        )
        return not bool(result)

    async def delete_message(self, chat_id: str, message_id: str) -> Any:
        result = await self._make_request(
            "deleteMessage", {"chat_id": chat_id, "message_id": str(message_id)}
        )
        return not bool(result)

    async def set_commands(self, commands: List[Dict[str, str]]) -> bool:
        result = await self._make_request("setCommands", {"bot_commands": commands})
        return not bool(result)

    async def update_bot_endpoints(self, url: str, endpoint_type: str):
        return await self._make_request(
            "updateBotEndpoints", {"url": url, "type": endpoint_type}
        )
    
    async def get_chat_member(self, chat_id: str, user_id: str):
        return await self._make_request(
            "getChatMember", {"chat_id": chat_id, "user_id": user_id}
        )
    
    async def pin_chat_message(self, chat_id: str, message_id: str, disable_notification: Optional[bool] = False):
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "disable_notification": disable_notification
        }
        return not bool(await self._make_request("pinChatMessage", payload))
    
    async def unpin_chat_message(self, chat_id: str, message_id: str):
        payload = {
            "chat_id": chat_id,
            "message_id": message_id
        }
        return not bool(await self._make_request("unpinChatMessage", payload))
    
    async def unpin_all_chat_messages(self, chat_id: str, message_id: str):
        payload = {
            "chat_id": chat_id,
            "message_id": message_id
        }
        return not bool(await self._make_request("unpinAllChatMessages", payload))

    async def get_chat_administrators(self, chat_id: str):
        return await self._make_request("getChatAdministrators", {"chat_id": chat_id})

    async def get_chat_member_count(self, chat_id: str):
        return await self._make_request("getChatMemberCount", {"chat_id": chat_id})

    async def ban_chat_member(self, chat_id: str, user_id: str):
        return await self._make_request(
            "banChatMember", {"chat_id": chat_id, "user_id": user_id}
        )

    async def unban_chat_member(self, chat_id: str, user_id: str):
        return await self._make_request(
            "unbanChatMember", {"chat_id": chat_id, "user_id": user_id}
        )

    async def get_chat_member(self, chat_id: str, user_id: str):
        return await self._make_request(
            "getChatMember", {"chat_id": chat_id, "user_id": user_id}
        )

    async def promote_chat_member(self, chat_id: str, user_id: str):
        raise NotImplementedError

    async def set_chat_permissions(
        self, chat_id: str, permissions: Optional[list] = None
    ):
        raise NotImplementedError

    async def edit_chat_keypad(
        self,
        chat_id: str,
        keypad_type: ChatKeypadTypeEnum,
        keypad: Optional[Keypad] = None,
    ) -> bool:
        payload = {"chat_id": chat_id, "chat_keypad_type": keypad_type.value}
        if keypad:
            payload["chat_keypad"] = dataclasses.asdict(keypad)
        return not bool(await self._make_request("editChatKeypad", payload))

    def on_update(self, *filters: Filter) -> Callable:
        def decorator(handler: Callable) -> Callable:
            filter_key = str(uuid.uuid4())
            if filter_key not in self.handlers:
                self.handlers[filter_key] = []
            self.handlers[filter_key].append((filters, handler))
            logger.info(
                "Registered handler %s with filters: %s",
                handler.__name__,
                filters,
            )
            return handler

        return decorator
    
    def add_handler(self, handler: Callable, *filters: Filter) -> str:
        """
        Register a new handler with given filters.

        Args:
            handler (Callable): The function to handle updates.
            *filters (Filter): One or more filters that must pass.

        Returns:
            str: Unique handler key (can be used to remove handler later).
        
        Example:
            key = bot.add_handler(my_handler, TextFilter("hello"))
        """
        handler_key = str(uuid.uuid4())
        if handler_key not in self.handlers:
            self.handlers[handler_key] = []
        self.handlers[handler_key].append((filters, handler))
        logger.info(
            "Handler %s added with key %s, filters: %s",
            handler.__name__,
            handler_key,
            filters,
        )
        return handler_key

    def remove_handler(self, handler_key: str, handler: Optional[Callable] = None) -> bool:
        """
        Remove a registered handler.

        Args:
            handler_key (str): The unique key returned by add_handler/on_update.
            handler (Optional[Callable]): Specific handler function to remove.
                                          If None, removes all handlers under the key.

        Returns:
            bool: True if something was removed, False otherwise.

        Example:
            bot.remove_handler(key)
        """
        if handler_key not in self.handlers:
            return False

        if handler:
            before = len(self.handlers[handler_key])
            self.handlers[handler_key] = [
                (filters, h) for filters, h in self.handlers[handler_key] if h != handler
            ]
            after = len(self.handlers[handler_key])
            removed = before != after
            if not self.handlers[handler_key]:  # clean up empty key
                del self.handlers[handler_key]
            return removed
        else:
            del self.handlers[handler_key]
            return True

    def _parse_update(self, item: Dict) -> Optional[Union[Update, InlineMessage]]:
        update_type = item.get("type")
        if not update_type:
            logger.debug("Skipping update with no type: %r", item)
            return None

        chat_id = item.get("chat_id", "")
        if update_type == UpdateTypeEnum.RemovedMessage:
            return Update(
                client=self,
                type=UpdateTypeEnum.RemovedMessage,
                chat_id=chat_id,
                removed_message_id=str(item.get("removed_message_id", "")),
            )
        elif update_type in [
            UpdateTypeEnum.NewMessage,
            UpdateTypeEnum.UpdatedMessage,
        ]:
            msg_key = (
                "new_message"
                if update_type == UpdateTypeEnum.NewMessage
                else "updated_message"
            )
            msg_data = item.get(msg_key)
            if not msg_data:
                logger.debug("Skipping %s with no message data: %r", msg_key, item)
                return None

            msg_data["message_id"] = str(msg_data.get("message_id", ""))
            try:
                message_obj = Message(**msg_data)
                # message_obj = Message.from_dict(msg_data)
                return Update(
                    type=update_type,
                    chat_id=chat_id,
                    client=self,
                    new_message=(
                        message_obj
                        if update_type == UpdateTypeEnum.NewMessage
                        else None
                    ),
                    updated_message=(
                        message_obj
                        if update_type == UpdateTypeEnum.UpdatedMessage
                        else None
                    ),
                )
            except Exception as e:
                logger.exception("Failed to parse message: %r", msg_data)
                return None
        elif update_type == "InlineMessage":
            try:
                inline_msg = InlineMessage(
                    sender_id=item.get("sender_id", ""),
                    text=item.get("text", ""),
                    message_id=str(item.get("message_id", "")),
                    chat_id=chat_id,
                    file=item.get("file"),
                    location=item.get("location"),
                    aux_data=item.get("aux_data"),
                    client=self,
                )
                logger.info("Parsed InlineMessage: %s", inline_msg)
                return inline_msg
            except Exception as e:
                logger.exception("Failed to parse InlineMessage: %r", item)
                return None
        else:
            logger.debug("Unhandled update type: %s, data: %r", update_type, item)
            return None

    async def process_update(self, update: Union[Update, InlineMessage]):
        """Run middlewares in order before dispatching the update."""
        async def run_middlewares(index: int):
            if index < len(self.middlewares):
                mw = self.middlewares[index]
                if inspect.iscoroutinefunction(mw):
                    await mw(self, update, lambda: run_middlewares(index + 1))
                else:
                    mw(
                        self,
                        update,
                        lambda: asyncio.create_task(run_middlewares(index + 1)),
                    )
            else:
                await self._dispatch_update(update)

        await run_middlewares(0)

    async def _dispatch_update(self, update: Union[Update, InlineMessage]):
        """Invoke the first matching handler for the provided update."""
        update_type = "InlineMessage" if isinstance(update, InlineMessage) else update.type
        message_id = self._extract_message_id(update)

        # Create a unique key combining message_id and update_type to allow
        # processing both NewMessage and UpdatedMessage for the same message_id
        if isinstance(update, Update) and message_id:
            dedup_key = f"{message_id}:{update.type}"
            if dedup_key in self.processed_messages:
                logger.debug("Skipping duplicate update: %s", dedup_key)
                return
            self.processed_messages.append(dedup_key)
            logger.debug("Processing update: %s", dedup_key)

        loop = asyncio.get_running_loop()

        handler_found = False
        for filter_key, handler_list in self.handlers.items():
            for filters, handler in handler_list:
                if await self._filters_pass(update, filters):
                    handler_found = True
                    logger.debug("Handler %s matched for update %s", handler.__name__, update_type)
                    if asyncio.iscoroutinefunction(handler):
                        asyncio.create_task(handler(self, update))
                    else:
                        loop.run_in_executor(None, handler, self, update)
                    return
        
        if not handler_found:
            logger.debug("No handler found for update type: %s", update_type)

    def _extract_message_id(
        self, update: Union[Update, InlineMessage]
    ) -> Optional[str]:
        if isinstance(update, InlineMessage):
            return update.message_id
        if isinstance(update, Update):
            if update.type == UpdateTypeEnum.RemovedMessage:
                return update.removed_message_id
            if update.new_message:
                return update.new_message.message_id
            if update.updated_message:
                return update.updated_message.message_id
        return None

    async def _filters_pass(
        self, update: Union[Update, InlineMessage], filters: Tuple[Filter, ...]
    ) -> bool:
        update_type = ("InlineMessage" if isinstance(update, InlineMessage) else update.type)

        for f in filters:
            if isinstance(f, type):
                f = f()

            result = await f.check(update)
            logger.debug(
                "Filter %s check for update %s: %s",
                f.__class__.__name__,
                update_type,
                result,
            )
            if not result:
                return False

        logger.debug("All filters passed for update %s", update_type)
        return True

    async def handle_webhook(self, request: web.Request) -> web.Response:
        """Process incoming webhook requests and queue updates for handling."""
        if request.method != "POST":
            logger.error("Invalid method: %s", request.method)
            return web.Response(status=405, text="Method Not Allowed")

        try:
            data = await request.json()
            logger.debug(
                "Webhook payload for %s: %s",
                request.path,
                json.dumps(data, ensure_ascii=False),
            )
            updates = []

            # Handle inline_message
            if "inline_message" in data:
                try:
                    inline_msg = InlineMessage(
                        sender_id=data["inline_message"].get("sender_id", ""),
                        text=data["inline_message"].get("text", ""),
                        message_id=str(data["inline_message"].get("message_id", "")),
                        chat_id=data["inline_message"].get("chat_id", ""),
                        file=data["inline_message"].get("file"),
                        location=data["inline_message"].get("location"),
                        aux_data=data["inline_message"].get("aux_data"),
                        client=self,
                    )
                    logger.info("Received InlineMessage: %s", inline_msg)
                    updates.append(inline_msg)
                except Exception:
                    logger.exception("Failed to parse InlineMessage payload")

            # Handle updates
            elif "update" in data:
                update = self._parse_update(data["update"])
                if update:
                    logger.info("Received Update: %s", update)
                    updates.append(update)

            for update in updates:
                logger.debug("Queuing update for processing: %s", update)
                asyncio.create_task(self.process_update(update))

            return web.json_response({"status": "OK"})
        except json.JSONDecodeError:
            logger.error("Invalid JSON in webhook request")
            return web.json_response(
                {"status": "ERROR", "error": "Invalid JSON"}, status=400
            )
        except Exception as e:
            logger.error("Webhook error for %s: %s", request.path, e)
            return web.json_response({"status": "ERROR", "error": str(e)}, status=500)

    async def run(
        self,
        webhook_url: Optional[str] = None,
        path: Optional[str] = "/webhook",
        host: str = "0.0.0.0",
        port: int = 8080,
    ):
        """Run the client in either webhook or polling mode."""
        self.use_webhook = bool(webhook_url)
        await self.start()
        if self.use_webhook:
            app = web.Application()
            webhook_base = path.rstrip("/")
            app.router.add_post(f"{webhook_base}", self.handle_webhook)
            app.router.add_post(f"{webhook_base}/receiveUpdate", self.handle_webhook)
            app.router.add_post(f"{webhook_base}/receiveInlineMessage", self.handle_webhook)
            app.router.add_post(f"{webhook_base}/receiveQuery", self.handle_webhook)
            app.router.add_post(f"{webhook_base}/getSelectionItem", self.handle_webhook)
            app.router.add_post(f"{webhook_base}/searchSelectionItems", self.handle_webhook)

            webhook_url = f"{webhook_url.rstrip('/')}{webhook_base}"
            for endpoint_type in [
                "ReceiveUpdate",
                "ReceiveInlineMessage",
                "ReceiveQuery",
                "GetSelectionItem",
                "SearchSelectionItems",
            ]:
                response = await self.update_bot_endpoints(webhook_url, endpoint_type)
                logger.info(
                    "Webhook set for %s to %s: %s",
                    endpoint_type,
                    webhook_url,
                    response,
                )

            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, host, port)
            await site.start()
            logger.info(
                "Webhook server running at http://%s:%s%s",
                host,
                port,
                webhook_base,
            )
            try:
                while self.running:
                    await asyncio.sleep(1)
            finally:
                await runner.cleanup()
        else:
            idle_delay = self.poll_interval
            max_idle_delay = max(self.long_poll_timeout, self.poll_interval * 8)
            while self.running:
                try:
                    updates = await self.updater(
                        limit=100, poll_timeout=self.long_poll_timeout
                    )
                    if not updates:
                        await asyncio.sleep(idle_delay)
                        idle_delay = min(max_idle_delay, idle_delay * 1.5)
                        continue

                    idle_delay = self.poll_interval
                    for update in updates:
                        logger.debug("Processing polled update: %s", update)
                        asyncio.create_task(self.process_update(update))
                except Exception as e:
                    logger.error("Polling error: %s", e)
                    await asyncio.sleep(idle_delay)
                    idle_delay = min(max_idle_delay, idle_delay * 2)

    async def close(self):
        """Close the underlying HTTP session."""
        await self._close_session()

    async def download_file(
        self,
        file_id: str,
        save_as: Optional[str] = None,
        progress: Optional[Callable[[int, int], None]] = None,
        chunk_size: int = 65536,
        as_bytes: bool = False,
        file_name: Optional[str] = None,
        timeout: Optional[Union[int, float]] = 20.0,
    ) -> Union[str, bytes, None]:
        """
        Downloads a file by file_id.

        Args:
            file_id (str): Unique identifier of the file.
            save_as (Optional[str]): File path to save. Ignored if as_bytes=True.
            progress (Optional[Callable[[int, int], None]]): Optional progress callback.
            chunk_size (int): Download chunk size in bytes.
            as_bytes (bool): If True, returns the content as bytes instead of saving.
            file_name (Optional[str]): File name to save. Ignored if save_as is provided.
            timeout (Optional[Union[int, float]]): Timeout for the download request.
        Returns:
            str: Path to saved file (if as_bytes=False)
            bytes: Content of the file (if as_bytes=True)
        """
        try:
            download_url = await self.get_file(file_id)
        except Exception:
            raise ValueError(f"Invalid file_id: {file_id}")

        if not download_url:
            raise ValueError(f"Invalid download file url: {download_url}")

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            async with session.get(download_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to download file: {response.status}")

                content_type = response.headers.get("Content-Type", "")
                ext = mimetypes.guess_extension(content_type)
                ext = ext if ext else ""
                total_size = int(response.headers.get("Content-Length", 0))
                downloaded = 0

                if as_bytes:
                    content = bytearray()
                    async for chunk in response.content.iter_chunked(chunk_size):
                        content.extend(chunk)
                        downloaded += len(chunk)
                        if progress:
                            try:
                                progress(downloaded, total_size)
                            except Exception:
                                pass
                    return bytes(content)
                else:
                    if save_as is None:
                        save_as = file_name

                    with open(save_as, "wb") as f:
                        async for chunk in response.content.iter_chunked(chunk_size):
                            f.write(chunk)
                            downloaded += len(chunk)
                            if progress:
                                try:
                                    progress(downloaded, total_size)
                                except Exception:
                                    pass

                    return save_as


def get_extension(content_type: str) -> str:
    """Convert MIME type to file extension (e.g., image/jpeg -> .jpg)."""
    ext = mimetypes.guess_extension(content_type)
    return ext if ext else ""
