from typing import Literal, List, Optional
from .types import *

from .. import exceptions
import rubpy

class Bot:
    BASE_URL = 'https://messengerg2b1.iranlms.ir/v3/'

    def __init__(self, client: "rubpy.Client") -> None:
        self.client = client
        self.url = f'{self.BASE_URL}{client.bot_token}/'

    async def execute(self, method: str, data: dict):
        result = await self.client.connection.send(
            api_version='bot',
            url=self.url + method,
            input=data,
        )

        if result.get('status') != 'OK':
            raise exceptions.APIException(result)

        return result.get('data')

    async def _send_message(self, method: str, data: dict) -> str:
        res = await self.execute(method=method, data=data)
        return res['message_id']

    async def get_me(self) -> Bot:
        bot = await self.execute(method='getMe', data={})
        return Bot(**bot)

    async def send_message(
        self,
        chat_id: str,
        text: str,
        chat_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        inline_keypad: Optional[Keypad] = None,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: Literal[None, 'New', 'Remove'] = None,
    ) -> str:
        data = {
            'text': text,
            'chat_id': chat_id,
            'disable_notification': disable_notification
        }
        if chat_keypad:
            data['chat_keypad'] = chat_keypad.dict()
            data['chat_keypad_type'] = chat_keypad_type
        if inline_keypad:
            data['inline_keypad'] = inline_keypad.dict()
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id

        return await self._send_message(method='sendMessage', data=data)

    async def send_poll(
        self,
        chat_id: str,
        question: str,
        options: List[str],
        chat_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        inline_keypad: Optional[Keypad] = None,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: Literal[None, 'New', 'Remove'] = None,
    ) -> str:
        data = {
            'chat_id': chat_id,
            'options': options,
            'question': question,
            'chat_keypad': chat_keypad,
            'inline_keypad': inline_keypad,
            'chat_keypad_type': chat_keypad_type,
            'reply_to_message_id': reply_to_message_id,
            'disable_notification': disable_notification,
        }

        return await self._send_message(method='sendPoll', data=data)

    async def send_location(
        self,
        chat_id: str,
        latitude: str,
        longitude: str,
        chat_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        inline_keypad: Optional[Keypad] = None,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: Literal[None, 'New', 'Remove'] = None,
    ) -> str:
        data = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
            'chat_keypad': chat_keypad,
            'disable_notification': disable_notification,
            'inline_keypad': inline_keypad,
            'reply_to_message_id': reply_to_message_id,
            'chat_keypad_type': chat_keypad_type,
        }

        return await self._send_message(method='sendLocation', data=data)

    async def send_sticker(
        self,
        chat_id: str,
        sticker_id: str,
        chat_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        inline_keypad: Optional[Keypad] = None,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: Literal[None, 'New', 'Remove'] = None,
    ) -> str:
        data = {
            'chat_id': chat_id,
            'sticker_id': sticker_id,
            'chat_keypad': chat_keypad,
            'disable_notification': disable_notification,
            'inline_keypad': inline_keypad,
            'reply_to_message_id': reply_to_message_id,
            'chat_keypad_type': chat_keypad_type,
        }

        return await self._send_message(method='sendSticker', data=data)

    async def send_contact(
        self,
        chat_id: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        chat_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        inline_keypad: Optional[Keypad] = None,
        reply_to_message_id: Optional[str] = None,
        chat_keypad_type: Literal[None, 'New', 'Remove'] = None,
    ) -> str:
        data = {
            'chat_id': chat_id,
            'last_name': last_name,
            'first_name': first_name,
            'chat_keypad': chat_keypad,
            'phone_number': phone_number,
            'inline_keypad': inline_keypad,
            'chat_keypad_type': chat_keypad_type,
            'reply_to_message_id': reply_to_message_id,
            'disable_notification': disable_notification,
        }

        return await self._send_message(method='sendContact', data=data)

    async def upload(self, url: str, file_name: str, file_path: str) -> str:
        res = await self._send_multipart_request(url=url, form_data={'file': (file_name, open(file_path, 'rb'))})
        return res['file_id']

    async def get_file(self, file_id: str) -> str:
        data = {'file_id': file_id}
        res = await self.execute(method='getFile', data=data)
        return res['download_url']

    async def set_commands(self, bot_commands: List[BotCommand]) -> None:
        data = {'bot_commands': [command.dict() for command in bot_commands]}
        await self.execute(method='setCommands', data=data)

    async def edit_chat_keypad(self, chat_id: str, chat_keypad: Keypad) -> None:
        data = {
            'chat_id': chat_id,
            'chat_keypad_type': 'New',
            'chat_keypad': chat_keypad.dict(),
        }
        await self.execute(method='editChatKeypad', data=data)

    async def remove_chat_keypad(self, chat_id: str) -> None:
        data = {
            'chat_id': chat_id,
            'chat_keypad_type': 'Remove',
        }
        await self.execute(method='editChatKeypad', data=data)

    async def update_bot_endpoint(
            self,
            token: str,
            url: str,
            type: Literal['ReceiveUpdate', 'ReceiveInlineMessage', 'ReceiveQuery',
                        'GetSelectionItem', 'SearchSelectionItems'],
    ):# -> Final[Union['Done', 'InvalidUrl']]:
        data = {
            'url': url,
            'type': type,
        }
        res = await self.execute(method='updateBotEndpoints', data=data)
        return res['status']

        # ... (previous code)

    async def forward_message(
            self,
            from_chat_id: str,
            message_id: str,
            to_chat_id: str,
            disable_notification: bool = False
    ) -> str:
        data = {
            'from_chat_id': from_chat_id,
            'message_id': message_id,
            'to_chat_id': to_chat_id,
            'disable_notification': disable_notification,
        }
        res = await self.execute(method='forwardMessage', data=data)
        return res['new_message_id']

    async def edit_message_text(self, chat_id: str, message_id: str, text: str) -> None:
        data = {
            'text': text,
            'chat_id': chat_id,
            'message_id': message_id,
        }
        await self.execute(method='editMessageText', data=data)

    async def edit_message_keypad(self, chat_id: str, message_id: str, inline_keypad: Keypad) -> None:
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'inline_keypad': inline_keypad.dict(),
        }
        await self.execute(method='editMessageKeypad', data=data)

    async def delete_message(self, chat_id: str, message_id: str) -> None:
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
        }
        await self.execute(method='deleteMessage', data=data)

    async def send_file(
            self,
            token: str,
            chat_id: str,
            file_id: str,
            chat_keypad: Optional[Keypad] = None,
            disable_notification: bool = False,
            inline_keypad: Optional[Keypad] = None,
            reply_to_message_id: Optional[str] = None,
            chat_keypad_type: Literal[None, 'New', 'Remove'] = None,
    ) -> str:
        data = {
            'chat_id': chat_id,
            'file_id': file_id,
            'chat_keypad': chat_keypad,
            'disable_notification': disable_notification,
            'inline_keypad': inline_keypad,
            'reply_to_message_id': reply_to_message_id,
            'chat_keypad_type': chat_keypad_type,

        }
        res = await self.execute(method='sendFile', data=data)
        return res['message_id']

    async def request_send_file(self, type: Literal['File', 'Image', 'Voice', 'Music', 'Gif']) -> str:
        data = {
            'type': type,
        }
        res = await self.execute(method='requestSendFile', data=data)
        return res['upload_url']

    async def upload(self, url: str, file_name: str, file_path: str) -> str:
        res = await self._send_multipart_request(url=url, form_data={'file': (file_name, open(file_path, 'rb'))})
        return res['file_id']

    async def get_file(self, file_id: str) -> str:
        data = {'file_id': file_id}
        res = await self.execute(method='getFile', data=data)
        return res['download_url']

    async def set_commands(self, bot_commands: List[BotCommand]) -> None:
        data = {'bot_commands': [command.dict() for command in bot_commands]}
        await self.execute(method='setCommands', data=data)

    async def edit_chat_keypad(self, chat_id: str, chat_keypad: Keypad) -> None:
        data = {
            'chat_id': chat_id,
            'chat_keypad_type': 'New',
            'chat_keypad': chat_keypad.dict(),
        }
        await self.execute(method='editChatKeypad', data=data)

    async def remove_chat_keypad(self, chat_id: str) -> None:
        data = {
            'chat_id': chat_id,
            'chat_keypad_type': 'Remove',
        }
        await self.execute(method='editChatKeypad', data=data)

    async def update_bot_endpoint(
            self,
            url: str,
            type: Literal['ReceiveUpdate', 'ReceiveInlineMessage', 'ReceiveQuery',
                        'GetSelectionItem', 'SearchSelectionItems'],
    ): # -> Final[Union['Done', 'InvalidUrl']]:
        data = {
            'url': url,
            'type': type,
        }
        res = await self.execute(method='updateBotEndpoints', data=data)
        return res['status']

# ... (remaining code)
