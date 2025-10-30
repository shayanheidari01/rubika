import asyncio
import dataclasses
import inspect
import mimetypes
from pathlib import Path
import threading
import aiohttp
from aiohttp import web
import json
from typing import Any, Callable, Dict, List, Literal, Optional, Union, Tuple
import logging
from collections import deque
import time
import uuid

from rubpy.bot.enums import ChatKeypadTypeEnum, UpdateTypeEnum
from rubpy.bot.filters import Filter
from rubpy.bot.models import (
    Keypad,
    InlineMessage,
    Update,
    Message,
    MessageId,
    Chat,
    Bot,
)
from rubpy.bot.exceptions import APIException

# Setup logging
# logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def has_time_passed(last_time, seconds: int = 5) -> bool:
    try:
        timestamp = int(float(last_time))
        now = time.time()
        return (now - timestamp) > seconds
    except (TypeError, ValueError):
        return False


class BotClient:
    BASE_URL = "https://botapi.rubika.ir/v3/{}/"

    def __init__(
            self,
            token: str,
            rate_limit: float = 0.5,
            use_webhook: bool = False,
            timeout: Union[int, float] = 10.0,
            connector: "aiohttp.TCPConnector" = None
    ) -> None:

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
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.first_get_updates = True
        self.use_webhook = use_webhook
        self.timeout = timeout
        self.connector = connector
        logger.info("Rubika client initialized, use_webhook=%s", use_webhook)

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
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.stop()
    
    def __enter__(self) -> "BotClient":
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.stop()

    async def _rate_limit_delay(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            await asyncio.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()

    async def start(self):
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            connector = self.connector or aiohttp.TCPConnector(limit=50, limit_per_host=10)
            self.session = aiohttp.ClientSession(timeout=timeout, connector=connector)
        self.running = True

        for handler in self.start_handlers:
            if inspect.iscoroutinefunction(handler):
                await handler(self)
            else:
                handler(self)

        logger.info("RubikaPY bot client started")

    async def stop(self):
        if self.session and not self.session.closed:
            await self.session.close()
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
            logger.info(f"Middleware {func.__name__} registered")
            return func
        return decorator

    async def _make_request(self, method: str, data: Dict) -> Dict:
        await self._rate_limit_delay()
        url = f"{self.base_url}{method}"
        
        async with self.session.post(url, json=data) as response:
            if not response.ok:
                raise

            result = await response.json()
            logger.debug(f"API response for {method}: {result}")

            if result["status"] != "OK":
                raise APIException(
                    status=result["status"],
                    dev_message=result.get("dev_message")
                )
            
            return result["data"]

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
            content_type="application/octet-stream",  # یا نوع فایل واقعی مثل image/png
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=form, ssl=False) as res:
                if res.status != 200:
                    text = await res.text()
                    raise aiohttp.ClientResponseError(
                        res.request_info, res.history, status=res.status, message=text
                    )

                data = await res.json()
                return data["data"]["file_id"]  # اطمینان حاصل کن که ساختار JSON این‌طوریه

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
        # ساخت دیتا به صورت مستقیم (کاهش شرط اضافی)
        data = {"limit": limit, **({"offset_id": offset_id} if offset_id else {})}

        response = await self._make_request("getUpdates", data)
        updates_raw = response.get("updates")
        if not updates_raw:
            return []

        # ساخت لیست با list comprehension (سریع‌تر از for)
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
        self, limit: int = 100, offset_id: str = ""
    ) -> List[Union[Update, InlineMessage]]:
        data = {"limit": limit}
        updates = []
        if offset_id or self.next_offset_id:
            data["offset_id"] = self.next_offset_id if not offset_id else offset_id

        try:
            response = await self._make_request("getUpdates", data)
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
                        and update.updated_message.time
                    )

                    # اگر از آخرین پیام بیشتر از 5 ثانیه گذشته، لیست update رو پاک کن
                    if has_time_passed(last_time, 5):
                        continue

                    updates.append(update)

        except Exception as e:
            logger.exception(f"Failed to get updates: {str(e)}")

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

    async def edit_message_text(self, chat_id: str, message_id: str, text: str) -> bool:
        result = await self._make_request(
            "editMessageText",
            {"chat_id": chat_id, "message_id": str(message_id), "text": text},
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
                f"Registered handler {handler.__name__} with filters: {filters}"
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
            f"Handler {handler.__name__} added with key {handler_key}, filters: {filters}"
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
            logger.debug(f"Skipping update with no type: {item}")
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
                logger.debug(f"Skipping {msg_key} with no message data: {item}")
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
                logger.error(f"Failed to parse message: {msg_data}, error: {str(e)}")
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
                logger.info(f"Parsed InlineMessage: {inline_msg}")
                return inline_msg
            except Exception as e:
                logger.error(f"Failed to parse InlineMessage: {item}, error: {str(e)}")
                return None
        else:
            logger.debug(f"Unhandled update type: {update_type}, data: {item}")
            return None

    async def process_update(self, update: Union[Update, InlineMessage]):
        async def run_middlewares(index: int):
            if index < len(self.middlewares):
                mw = self.middlewares[index]
                if inspect.iscoroutinefunction(mw):
                    await mw(self, update, lambda: run_middlewares(index + 1))
                else:
                    mw(self, update, lambda: asyncio.create_task(run_middlewares(index + 1)))
            else:
                await self._dispatch_update(update)

        await run_middlewares(0)

    async def _dispatch_update(self, update: Union[Update, InlineMessage]):
        update_type = "InlineMessage" if isinstance(update, InlineMessage) else update.type
        message_id = self._extract_message_id(update)

        if isinstance(update, Update) and message_id and message_id in self.processed_messages:
            return
        if message_id and isinstance(update, Update):
            self.processed_messages.append(message_id)

        for filter_key, handler_list in self.handlers.items():
            for filters, handler in handler_list:
                if await self._filters_pass(update, filters):
                    if asyncio.iscoroutinefunction(handler):
                        asyncio.create_task(handler(self, update))
                    else:
                        threading.Thread(target=handler, args=(self, update)).start()
                    return

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
            logger.info(f"Filter {f.__class__.__name__} check for update {update_type}: {result}")
            if not result:
                return False

        logger.info(f"All filters passed for update {update_type}")
        return True

    async def handle_webhook(self, request: web.Request) -> web.Response:
        if request.method != "POST":
            logger.error(f"Invalid method: {request.method}")
            return web.Response(status=405, text="Method Not Allowed")

        try:
            data = await request.json()
            logger.debug(
                f"Webhook payload for {request.path}: {json.dumps(data, ensure_ascii=False)}"
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
                    logger.info(f"Received InlineMessage: {inline_msg}")
                    updates.append(inline_msg)
                except Exception as e:
                    logger.error(f"Failed to parse InlineMessage: {str(e)}")

            # Handle updates
            elif "update" in data:
                update = self._parse_update(data["update"])
                if update:
                    logger.info(f"Received Update: {update}")
                    updates.append(update)

            for update in updates:
                logger.info(f"Queuing update for processing: {update}")
                asyncio.create_task(self.process_update(update))

            return web.json_response({"status": "OK"})
        except json.JSONDecodeError:
            logger.error("Invalid JSON in webhook request")
            return web.json_response(
                {"status": "ERROR", "error": "Invalid JSON"}, status=400
            )
        except Exception as e:
            logger.error(f"Webhook error for {request.path}: {str(e)}")
            return web.json_response({"status": "ERROR", "error": str(e)}, status=500)

    async def run(
        self,
        webhook_url: Optional[str] = None,
        path: Optional[str] = "/webhook",
        host: str = "0.0.0.0",
        port: int = 8080
    ):
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
            for endpoint_type in ["ReceiveUpdate", "ReceiveInlineMessage", "ReceiveQuery", "GetSelectionItem", "SearchSelectionItems"]:
                response = await self.update_bot_endpoints(webhook_url, endpoint_type)
                logger.info(
                    f"Webhook set for {endpoint_type} to {webhook_url}: {response}"
                )

            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, host, port)
            await site.start()
            logger.info(f"Webhook server running at http://{host}:{port}{webhook_base}")
            try:
                while self.running:
                    await asyncio.sleep(1)
            finally:
                await runner.cleanup()
        else:
            while self.running:
                try:
                    updates = await self.updater(limit=100)
                    for update in updates:
                        logger.info(f"Processing polled update: {update}")
                        asyncio.create_task(self.process_update(update))
                except Exception as e:
                    logger.error(f"Polling error: {str(e)}")

    async def close(self):
        if not self.session.closed:
            await self.session.close()

    async def download_file(
        self,
        file_id: str,
        save_as: Optional[str] = None,
        progress: Optional[Callable[[int, int], None]] = None,
        chunk_size: int = 65536,
        as_bytes: bool = False,
        timeout: Optional[Union[int, float]] = 20.0
    ) -> Union[str, bytes, None]:
        """
        Downloads a file by file_id.

        Args:
            file_id (str): Unique identifier of the file.
            save_as (Optional[str]): File path to save. Ignored if as_bytes=True.
            progress (Optional[Callable[[int, int], None]]): Optional progress callback.
            chunk_size (int): Download chunk size in bytes.
            as_bytes (bool): If True, returns the content as bytes instead of saving.

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
                        save_as = f"{file_id}{ext}"

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
