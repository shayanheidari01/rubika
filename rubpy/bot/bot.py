import asyncio
import dataclasses
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
from rubpy.bot.models import Keypad, InlineMessage, Update, Message
from rubpy.bot.models.bot import Bot
from rubpy.bot.models.chat import Chat
from rubpy.bot.models.message import MessageId

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
    def __init__(self, token: str, rate_limit: float = 0.5, use_webhook: bool = False):
        self.token = token
        self.base_url = f"https://botapi.rubika.ir/v3/{token}/"
        self.handlers: Dict[str, List[Tuple[Tuple[Filter, ...], Callable]]] = {}
        self.session = None
        self.running = False
        self.next_offset_id = None
        self.processed_messages = deque(maxlen=10000)
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.first_get_updates = True
        self.use_webhook = use_webhook
        logger.info("Rubika client initialized, use_webhook=%s", use_webhook)

    async def _rate_limit_delay(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            await asyncio.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()

    async def start(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        self.running = True
        logger.info("Rubika client started")

    async def stop(self):
        if self.session and not self.session.closed:
            await self.session.close()
        self.running = False
        logger.info("Rubika client stopped")

    async def _make_request(self, method: str, data: Dict) -> Dict:
        await self._rate_limit_delay()
        url = f"{self.base_url}{method}"
        try:
            async with self.session.post(url, json=data) as response:
                if response.status != 200:
                    text = await response.text()
                    logger.error(f"Request failed: {method} status={response.status} body={text}")
                    raise aiohttp.ClientResponseError(response.request_info, response.history, status=response.status, message=text)
                result = await response.json()
                logger.debug(f"API response for {method}: {result}")

                if result['status'] != 'OK':
                    logger.error(f"API error in {method}: {result}")
                    raise
                return result['data']
        except Exception as e:
            logger.error(f"Error in _make_request for {method}: {str(e)}")
            return {"status": "ERROR", "error": str(e)}

    async def get_me(self) -> Bot:
        result = await self._make_request('getMe', {})
        return Bot(**result['bot'])

    async def send_message(
        self,
        chat_id: str,
        text: str,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE
    ) -> MessageId:
        payload = {
            'chat_id': chat_id,
            'text': text,
            'disable_notification': disable_notification,
            'chat_keypad_type': chat_keypad_type.value,
        }
        if chat_keypad:
            payload['chat_keypad'] = dataclasses.asdict(chat_keypad)
        if inline_keypad:
            payload['inline_keypad'] = dataclasses.asdict(inline_keypad)
        if reply_to_message_id:
            payload['reply_to_message_id'] = str(reply_to_message_id)

        result = await self._make_request('sendMessage', payload)
        result['chat_id'] = chat_id
        result['client'] = self
        return MessageId(**result)

    async def send_sticker(
        self,
        chat_id: str,
        sticker_id: str,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE
    ) -> MessageId:
        payload = {
            'chat_id': chat_id,
            'sticker_id': sticker_id,
            'disable_notification': disable_notification,
            'chat_keypad_type': chat_keypad_type.value,
        }
        if chat_keypad:
            payload['chat_keypad'] = dataclasses.asdict(chat_keypad)
        if inline_keypad:
            payload['inline_keypad'] = dataclasses.asdict(inline_keypad)
        if reply_to_message_id:
            payload['reply_to_message_id'] = str(reply_to_message_id)

        result = await self._make_request('sendSticker', payload)
        result['chat_id'] = chat_id
        result['client'] = self
        return MessageId(**result)
    
    async def send_file(
        self,
        chat_id: str,
        file: Optional[Union[str, Path]] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        file_name: Optional[str] = None,
        type: Literal['File', 'Image', 'Voice', 'Music', 'Gif', 'Video'] = 'File',
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE
    ) -> MessageId:
        if file:
            file_name = file_name or Path(file).name
            upload_url = await self.request_send_file(type)
            file_id = await self.upload_file(upload_url, file_name, file)

        payload = {
            'chat_id': chat_id,
            'file_id': file_id,
            'text': text,
            'disable_notification': disable_notification,
            'chat_keypad_type': chat_keypad_type.value,
        }
        if chat_keypad:
            payload['chat_keypad'] = dataclasses.asdict(chat_keypad)
        if inline_keypad:
            payload['inline_keypad'] = dataclasses.asdict(inline_keypad)
        if reply_to_message_id:
            payload['reply_to_message_id'] = str(reply_to_message_id)

        result = await self._make_request('sendFile', payload)
        result['chat_id'] = chat_id
        result['client'] = self
        result['file_id'] = file_id
        return MessageId(**result)
    
    async def request_send_file(self, type: Literal['File', 'Image', 'Voice', 'Music', 'Gif', 'Video']) -> str:
        if type not in ['File', 'Image', 'Voice', 'Music', 'Gif', 'Video']:
            raise ValueError("type is just be in ['File', 'Image', 'Voice', 'Music', 'Gif', 'Video']")

        result = await self._make_request('requestSendFile', {'type': type})
        return result['upload_url']
    
    async def upload_file(self, url: str, file_name: str, file_path: str) -> str:
        form = aiohttp.FormData()
        form.add_field(
            name='file',
            value=open(file_path, 'rb'),
            filename=file_name,
            content_type='application/octet-stream'  # یا نوع فایل واقعی مثل image/png
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=form, ssl=False) as res:
                if res.status != 200:
                    text = await res.text()
                    raise aiohttp.ClientResponseError(
                        res.request_info, res.history, status=res.status, message=text
                    )

                data = await res.json()
                return data['data']['file_id']  # اطمینان حاصل کن که ساختار JSON این‌طوریه
    
    async def get_file(self, file_id: str) -> str:
        result = await self._make_request('getFile', {'file_id': file_id})
        return result['download_url']

    async def send_poll(self, chat_id: str, question: str, options: List[str]) -> MessageId:
        result = await self._make_request('sendPoll', {'chat_id': chat_id, 'question': question, 'options': options})
        result['chat_id'] = chat_id
        result['client'] = self
        return MessageId(**result)
    
    async def send_location(
        self,
        chat_id: str,
        latitude: Union[str, float],
        longitude: Union[str, float],
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE
    ) -> MessageId:
        payload = {'chat_id': chat_id, 'latitude': str(latitude), 'longitude': str(longitude),
                   "disable_notification": disable_notification,
                    "chat_keypad_type": chat_keypad_type.value}
        if chat_keypad:
            payload["chat_keypad"] = dataclasses.asdict(chat_keypad)
        if inline_keypad:
            payload["inline_keypad"] = dataclasses.asdict(inline_keypad)
        if reply_to_message_id:
            payload["reply_to_message_id"] = str(reply_to_message_id)
        result = await self._make_request('sendLocation', payload)
        result['chat_id'] = chat_id
        result['client'] = self
        return MessageId(**result)

    async def send_contact(
        self,
        chat_id: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE
    ) -> MessageId:
        payload = {
            'chat_id': chat_id,
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number,
            "disable_notification": disable_notification,
            "chat_keypad_type": chat_keypad_type.value
        }

        if chat_keypad:
            payload["chat_keypad"] = dataclasses.asdict(chat_keypad)
        if inline_keypad:
            payload["inline_keypad"] = dataclasses.asdict(inline_keypad)
        if reply_to_message_id:
            payload["reply_to_message_id"] = str(reply_to_message_id)
    
        result = await self._make_request('sendContact', payload)
        result['chat_id'] = chat_id
        result['client'] = self
        return MessageId(**result)

    async def get_updates(self, limit: int = 100, offset_id: str = "") -> List[Union[Update, InlineMessage]]:
        data = {"limit": limit}
        updates = []
        if offset_id:
            data["offset_id"] = offset_id
        response = await self._make_request("getUpdates", data)
        
        if response['updates']:
            for update in response['updates']:
                chat_id = update.get('chat_id', '')
                update = Update(
                    type=update.get('type', ''),
                    chat_id=chat_id,
                    client=self,
                    removed_message_id=str(update.get("removed_message_id", ""))
                )
                updates.append(update)

        return updates

    async def updater(self, limit: int = 100, offset_id: str = "") -> List[Union[Update, InlineMessage]]:
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
                    if update.type == UpdateTypeEnum.REMOVED_MESSAGE:
                        continue

                    last_time = (
                        getattr(update, 'new_message', None) and update.new_message.time
                    ) or (
                        getattr(update, 'updated_message', None) and update.updated_message.time
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

    async def get_chat(self, chat_id: str) -> Any:
        result = await self._make_request('getChat', {'chat_id': chat_id})
        return Chat(**result['chat'])

    async def forward_message(
        self,
        from_chat_id: str,
        message_id: str,
        to_chat_id: str,
        disable_notification: bool = False
    ) -> Any:
        result = await self._make_request(
            'forwardMessage',
            {'from_chat_id': from_chat_id, 'message_id': str(message_id), 'to_chat_id': to_chat_id, 'disable_notification': disable_notification}
        )
        result['chat_id'] = to_chat_id
        result['client'] = self
        return MessageId(**result)

    async def edit_message_text(self, chat_id: str, message_id: str, text: str) -> Any:
        result = await self._make_request('editMessageText', {'chat_id': chat_id, 'message_id': str(message_id), 'text': text})
        if result == {}:
            return True
        return False

    async def edit_message_keypad(self, chat_id: str, message_id: str, inline_keypad: Keypad) -> Any:
        result = await self._make_request('editMessageKeypad', {'chat_id': chat_id, 'message_id': str(message_id), 'inline_keypad': dataclasses.asdict(inline_keypad)})
        if result == {}:
            return True
        return False

    async def delete_message(self, chat_id: str, message_id: str) -> Any:
        result = await self._make_request('deleteMessage', {'chat_id': chat_id, 'message_id': str(message_id)})
        if result == {}:
            return True
        return False

    async def set_commands(self, commands: List[Dict[str, str]]) -> Any:
        result = await self._make_request('setCommands', {'bot_commands': commands})
        if result == {}:
            return True
        return False

    async def update_bot_endpoints(self, url: str, endpoint_type: str):
        return await self._make_request('updateBotEndpoints', {'url': url, 'type': endpoint_type})

    async def edit_chat_keypad(self, chat_id: str, keypad_type: ChatKeypadTypeEnum, keypad: Optional[Keypad] = None) -> Any:
        payload = {'chat_id': chat_id, 'chat_keypad_type': keypad_type.value}
        if keypad:
            payload['chat_keypad'] = dataclasses.asdict(keypad)
        result = await self._make_request('editChatKeypad', payload)
        if result == {}:
            return True
        return False

    def on_update(self, *filters: Filter) -> Callable:
        def decorator(handler: Callable) -> Callable:
            filter_key = str(uuid.uuid4())
            if filter_key not in self.handlers:
                self.handlers[filter_key] = []
            self.handlers[filter_key].append((filters, handler))
            logger.info(f"Registered handler {handler.__name__} with filters: {filters}")
            return handler
        return decorator

    def _parse_update(self, item: Dict) -> Optional[Union[Update, InlineMessage]]:
        update_type = item.get("type")
        if not update_type:
            logger.debug(f"Skipping update with no type: {item}")
            return None

        chat_id = item.get("chat_id", "")
        if update_type == UpdateTypeEnum.REMOVED_MESSAGE:
            return Update(
                client=self,
                type=UpdateTypeEnum.REMOVED_MESSAGE,
                chat_id=chat_id,
                removed_message_id=str(item.get("removed_message_id", ""))
            )
        elif update_type in [UpdateTypeEnum.NEW_MESSAGE, UpdateTypeEnum.UPDATED_MESSAGE]:
            msg_key = "new_message" if update_type == UpdateTypeEnum.NEW_MESSAGE else "updated_message"
            msg_data = item.get(msg_key)
            if not msg_data:
                logger.debug(f"Skipping {msg_key} with no message data: {item}")
                return None

            msg_data["message_id"] = str(msg_data.get("message_id", ""))
            try:
                message_obj = Message(**msg_data)
                #message_obj = Message.from_dict(msg_data)
                return Update(
                    type=update_type,
                    chat_id=chat_id,
                    client=self,
                    new_message=message_obj if update_type == UpdateTypeEnum.NEW_MESSAGE else None,
                    updated_message=message_obj if update_type == UpdateTypeEnum.UPDATED_MESSAGE else None
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
                    client=self
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
        update_type = "InlineMessage" if isinstance(update, InlineMessage) else update.type
        message_id = self._extract_message_id(update)

        # Skip processed messages check for InlineMessage to avoid issues with repeated message_id
        if isinstance(update, Update) and message_id and message_id in self.processed_messages:
            logger.debug(f"Skipping processed update ({update_type}): {message_id}")
            return

        if message_id and isinstance(update, Update):
            self.processed_messages.append(message_id)

        logger.info(f"Processing update: {update_type}, handlers available: {len(self.handlers)}")
        handled = False
        for filter_key, handler_list in self.handlers.items():
            logger.info(f"Checking handler list {filter_key} with {len(handler_list)} handlers")
            for filters, handler in handler_list:
                logger.info(f"Checking filters for handler {handler.__name__}: {filters}")
                if await self._filters_pass(update, filters):
                    try:
                        logger.info(f"Executing handler {handler.__name__} for update {update_type}")
                        if asyncio.iscoroutinefunction(handler):
                            asyncio.create_task(handler(self, update))
                        else:
                            threading.Thread(target=handler, args=(self, update,)).start()
                        handled = True
                    except Exception as e:
                        logger.exception(f"Error in handler {handler.__name__}: {str(e)}")
                else:
                    logger.info(f"Filters {filters} failed for handler {handler.__name__} on update {update_type}")
        if not handled:
            logger.warning(f"No handlers matched for update {update_type} with data: {update}")

    def _extract_message_id(self, update: Union[Update, InlineMessage]) -> Optional[str]:
        if isinstance(update, InlineMessage):
            return update.message_id
        if isinstance(update, Update):
            if update.type == UpdateTypeEnum.REMOVED_MESSAGE:
                return update.removed_message_id
            if update.new_message:
                return update.new_message.message_id
            if update.updated_message:
                return update.updated_message.message_id
        return None

    async def _filters_pass(self, update: Union[Update, InlineMessage], filters: Tuple[Filter, ...]) -> bool:
        update_type = "InlineMessage" if isinstance(update, InlineMessage) else update.type

        for f in filters:
            # اگر کلاس هست (و نه نمونه)، نمونه‌سازی کن
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
            logger.debug(f"Webhook payload for {request.path}: {json.dumps(data, ensure_ascii=False)}")
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
                        client=self
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
            return web.json_response({"status": "ERROR", "error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error(f"Webhook error for {request.path}: {str(e)}")
            return web.json_response({"status": "ERROR", "error": str(e)}, status=500)

    async def run(self, webhook_url: Optional[str] = None, path: Optional[str] = '/webhook', host: str = "0.0.0.0", port: int = 8080):
        self.use_webhook = bool(webhook_url)
        await self.start()
        if self.use_webhook:
            app = web.Application()
            webhook_base = path.rstrip('/')
            app.router.add_post(f"{webhook_base}", self.handle_webhook)
            app.router.add_post(f"{webhook_base}/receiveUpdate", self.handle_webhook)
            app.router.add_post(f"{webhook_base}/receiveInlineMessage", self.handle_webhook)
            
            webhook_url = f"{webhook_url.rstrip('/')}{webhook_base}"
            for endpoint_type in ["ReceiveUpdate", "ReceiveInlineMessage"]:
                response = await self.update_bot_endpoints(webhook_url, endpoint_type)
                logger.info(f"Webhook set for {endpoint_type} to {webhook_url}: {response}")
            
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
                    await asyncio.sleep(0.1)
                except Exception as e:
                    logger.error(f"Polling error: {str(e)}")
                    await asyncio.sleep(2)
    
    async def close(self):
        if not self.session.closed:
            await self.session.close()