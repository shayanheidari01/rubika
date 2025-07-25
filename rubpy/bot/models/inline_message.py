from dataclasses import dataclass
from typing import Dict, Optional

import rubpy
from rubpy.bot.enums import ChatKeypadTypeEnum
from rubpy.bot.models.keypad import Keypad

from .dict_like import DictLike


@dataclass
class InlineMessage(DictLike):
    sender_id: Optional[str] = None
    text: Optional[str] = None
    message_id: Optional[str] = None
    chat_id: Optional[str] = None
    file: Optional[Dict] = None
    location: Optional[Dict] = None
    aux_data: Optional[Dict] = None
    client: "rubpy.BotClient" = None

    async def reply(
        self,
        text: str,
        chat_keypad: Optional["rubpy.bot.models.Keypad"] = None,
        inline_keypad: Optional["rubpy.bot.models.Keypad"] = None,
        disable_notification: bool = False,
        chat_keypad_type: "rubpy.bot.enums.ChatKeypadTypeEnum" = ChatKeypadTypeEnum.NONE,
        chat_id: str = None
    ):
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_message(
            chat_id=chat_id or self.chat_id,
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type
        )
    
    async def reply_file(
        self,
        file: Optional[str] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional["Keypad"] = None,
        inline_keypad: Optional["Keypad"] = None,
        disable_notification: bool = False,
        chat_keypad_type: "ChatKeypadTypeEnum" = ChatKeypadTypeEnum.NONE,
        chat_id: str = None
    ):
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_file(
            chat_id=chat_id or self.chat_id,
            file=file,
            file_id=file_id,
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type
        )

    async def reply_photo(
        self,
        file: Optional[str] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional["Keypad"] = None,
        inline_keypad: Optional["Keypad"] = None,
        disable_notification: bool = False,
        chat_keypad_type: "ChatKeypadTypeEnum" = ChatKeypadTypeEnum.NONE,
        chat_id: str = None
    ):
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_file(
            chat_id=chat_id or self.chat_id,
            file=file,
            file_id=file_id,
            text=text,
            type='Image',
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type
        )

    async def reply_voice(
        self,
        file: Optional[str] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional["Keypad"] = None,
        inline_keypad: Optional["Keypad"] = None,
        disable_notification: bool = False,
        chat_keypad_type: "ChatKeypadTypeEnum" = ChatKeypadTypeEnum.NONE,
        chat_id: str = None
    ):
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_file(
            chat_id=chat_id or self.chat_id,
            file=file,
            file_id=file_id,
            text=text,
            type='Image',
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type
        )

    async def reply_music(
        self,
        file: Optional[str] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional["Keypad"] = None,
        inline_keypad: Optional["Keypad"] = None,
        disable_notification: bool = False,
        chat_keypad_type: "ChatKeypadTypeEnum" = ChatKeypadTypeEnum.NONE,
        chat_id: str = None
    ):
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_file(
            chat_id=chat_id or self.chat_id,
            file=file,
            file_id=file_id,
            text=text,
            type='Music',
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type
        )

    async def reply_gif(
        self,
        file: Optional[str] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional["Keypad"] = None,
        inline_keypad: Optional["Keypad"] = None,
        disable_notification: bool = False,
        chat_keypad_type: "ChatKeypadTypeEnum" = ChatKeypadTypeEnum.NONE,
        chat_id: str = None
    ):
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_file(
            chat_id=chat_id or self.chat_id,
            file=file,
            file_id=file_id,
            text=text,
            type='Gif',
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type
        )
    
    async def reply_video(
        self,
        file: Optional[str] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional["Keypad"] = None,
        inline_keypad: Optional["Keypad"] = None,
        disable_notification: bool = False,
        chat_keypad_type: "ChatKeypadTypeEnum" = ChatKeypadTypeEnum.NONE,
        chat_id: str = None
    ):
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_file(
            chat_id=chat_id or self.chat_id,
            file=file,
            file_id=file_id,
            text=text,
            type='Video',
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type
        )

    async def delete(self,
        chat_id: Optional[str] = None,
        message_id: Optional[str] = None
    ):
        return await self.client.delete_message(chat_id or self.chat_id, message_id or self.message_id)