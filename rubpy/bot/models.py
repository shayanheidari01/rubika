from dataclasses import dataclass
from typing import Callable, Optional, List, Union

import rubpy
from .dict_like import DictLike
from rubpy.enums import ParseMode
from .enums import (
    ChatKeypadTypeEnum,
    ChatTypeEnum,
    ForwardedFromEnum,
    PaymentStatusEnum,
    PollStatusEnum,
    LiveLocationStatusEnum,
    ButtonSelectionTypeEnum,
    ButtonCalendarTypeEnum,
    ButtonTextboxTypeKeypadEnum,
    ButtonTextboxTypeLineEnum,
    ButtonLocationTypeEnum,
    ButtonTypeEnum,
    UpdateTypeEnum,
)


@dataclass
class File(DictLike):
    file_id: Optional[str] = None
    file_name: Optional[str] = None
    size: Optional[str] = None


@dataclass
class Chat(DictLike):
    chat_id: Optional[str] = None
    chat_type: Optional[ChatTypeEnum] = None
    user_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    title: Optional[str] = None
    username: Optional[str] = None


@dataclass
class ForwardedFrom(DictLike):
    type_from: Optional[ForwardedFromEnum] = None
    message_id: Optional[str] = None
    from_chat_id: Optional[str] = None
    from_sender_id: Optional[str] = None


@dataclass
class PaymentStatus(DictLike):
    payment_id: Optional[str] = None
    status: Optional[PaymentStatusEnum] = None


@dataclass
class MessageTextUpdate(DictLike):
    message_id: Optional[str] = None
    text: Optional[str] = None


@dataclass
class Bot(DictLike):
    bot_id: Optional[str] = None
    bot_title: Optional[str] = None
    avatar: Optional[File] = None
    description: Optional[str] = None
    username: Optional[str] = None
    start_message: Optional[str] = None
    share_url: Optional[str] = None


@dataclass
class BotCommand(DictLike):
    command: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Sticker(DictLike):
    sticker_id: Optional[str] = None
    file: Optional[File] = None
    emoji_character: Optional[str] = None


@dataclass
class ContactMessage(DictLike):
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@dataclass
class PollStatus(DictLike):
    state: Optional[PollStatusEnum] = None
    selection_index: Optional[int] = None
    percent_vote_options: Optional[List[int]] = None
    total_vote: Optional[int] = None
    show_total_votes: Optional[bool] = None


@dataclass
class Poll(DictLike):
    question: Optional[str] = None
    options: Optional[List[str]] = None
    poll_status: Optional[PollStatus] = None


@dataclass
class Location(DictLike):
    longitude: Optional[str] = None
    latitude: Optional[str] = None


@dataclass
class LiveLocation(DictLike):
    start_time: Optional[str] = None
    live_period: Optional[int] = None
    current_location: Optional[Location] = None
    user_id: Optional[str] = None
    status: Optional[LiveLocationStatusEnum] = None
    last_update_time: Optional[str] = None


@dataclass
class ButtonSelectionItem(DictLike):
    text: Optional[str] = None
    image_url: Optional[str] = None
    type: Optional[ButtonSelectionTypeEnum] = None


@dataclass
class ButtonSelection(DictLike):
    selection_id: Optional[str] = None
    search_type: Optional[str] = None
    get_type: Optional[str] = None
    items: Optional[List[ButtonSelectionItem]] = None
    is_multi_selection: Optional[bool] = None
    columns_count: Optional[str] = None
    title: Optional[str] = None


@dataclass
class ButtonCalendar(DictLike):
    default_value: Optional[str] = None
    type: Optional[ButtonCalendarTypeEnum] = None
    min_year: Optional[str] = None
    max_year: Optional[str] = None
    title: Optional[str] = None


@dataclass
class ButtonNumberPicker(DictLike):
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    default_value: Optional[str] = None
    title: Optional[str] = None


@dataclass
class ButtonStringPicker(DictLike):
    items: Optional[List[str]] = None
    default_value: Optional[str] = None
    title: Optional[str] = None


@dataclass
class ButtonTextbox(DictLike):
    type_line: Optional[ButtonTextboxTypeLineEnum] = None
    type_keypad: Optional[ButtonTextboxTypeKeypadEnum] = None
    place_holder: Optional[str] = None
    title: Optional[str] = None
    default_value: Optional[str] = None


@dataclass
class ButtonLocation(DictLike):
    default_pointer_location: Optional[Location] = None
    default_map_location: Optional[Location] = None
    type: Optional[ButtonLocationTypeEnum] = None
    title: Optional[str] = None
    location_image_url: Optional[str] = None


@dataclass
class AuxData(DictLike):
    start_id: Optional[str] = None
    button_id: Optional[str] = None

@dataclass
class JoinChannelData(DictLike):
    username: Optional[str] = None
    ask_join: Optional[bool] = False

    def __post_init__(self):
        if self.username:
            self.username = self.username.replace('@', '')

@dataclass
class OpenChatData(DictLike):
    object_guid: Optional[str] = None
    object_type: Optional[ChatTypeEnum] = None

@dataclass
class ButtonLink(DictLike):
    type: Optional[str] = None
    link_url: Optional[str] = None
    joinchannel_data: Optional[JoinChannelData] = None
    open_chat_data: Optional[OpenChatData] = None

    def __post_init__(self):
        """Automatically normalize specific Rubika links to deep-link format."""
        if not self.link_url:
            return

        mappings = {
            "https://rubika.ir/joing/": "rubika://g.rubika.ir/",
            "https://rubika.ir/joinc/": "rubika://c.rubika.ir/",
            "https://rubika.ir/post/": "rubika://p.rubika.ir/"
        }

        for prefix, deep_prefix in mappings.items():
            if self.link_url.startswith(prefix):
                code = self.link_url[len(prefix):]
                self.link_url = deep_prefix + code
                break

@dataclass
class Button(DictLike):
    id: Optional[str] = None
    type: Optional[ButtonTypeEnum] = None
    button_text: Optional[str] = None
    button_selection: Optional[ButtonSelection] = None
    button_calendar: Optional[ButtonCalendar] = None
    button_number_picker: Optional[ButtonNumberPicker] = None
    button_string_picker: Optional[ButtonStringPicker] = None
    button_location: Optional[ButtonLocation] = None
    button_textbox: Optional[ButtonTextbox] = None
    button_link: Optional[ButtonLink] = None


@dataclass
class KeypadRow(DictLike):
    buttons: Optional[List[Button]] = None


@dataclass
class Keypad(DictLike):
    rows: Optional[List[KeypadRow]] = None
    resize_keyboard: Optional[bool] = None
    on_time_keyboard: Optional[bool] = None


@dataclass
class MessageKeypadUpdate(DictLike):
    message_id: Optional[str] = None
    inline_keypad: Optional[Keypad] = None


@dataclass
class MessageId(DictLike):
    message_id: Optional[str] = None
    new_message_id: Optional[str] = None
    file_id: Optional[str] = None
    chat_id: Optional[str] = None
    client: Optional["rubpy.BotClient"] = None

    async def delete(self):
        return await self.client.delete_message(
            self.chat_id, self.message_id or self.new_message_id
        )

    async def edit_text(self, new_text: str):
        return await self.client.edit_message_text(
            self.chat_id, self.message_id or self.new_message_id, new_text
        )


@dataclass
class MetaDataParts(DictLike):
    from_index: Optional[int] = None
    length: Optional[int] = None
    type: Optional[str] = None
    link_url: Optional[str] = None
    mention_text_user_id: Optional[str] = None

@dataclass
class Metadata(DictLike):
    meta_data_parts: Optional[List[MetaDataParts]] = None


@dataclass
class Message(DictLike):
    message_id: Optional[MessageId] = None
    time: Optional[str] = None
    text: Optional[str] = None
    is_edited: Optional[bool] = None
    sender_type: Optional[str] = None
    sender_id: Optional[str] = None
    aux_data: Optional[AuxData] = None
    file: Optional[File] = None
    reply_to_message_id: Optional[str] = None
    forwarded_from: Optional[ForwardedFrom] = None
    forwarded_no_link: Optional[str] = None
    location: Optional[Location] = None
    sticker: Optional[Sticker] = None
    contact_message: Optional[ContactMessage] = None
    poll: Optional[Poll] = None
    live_location: Optional[LiveLocation] = None
    metadata: Optional[Metadata] = None


@dataclass
class Update(DictLike):
    type: Optional[UpdateTypeEnum] = None
    chat_id: Optional[str] = None
    removed_message_id: Optional[str] = None
    new_message: Optional[Message] = None
    updated_message: Optional[Message] = None
    updated_payment: Optional[PaymentStatus] = None
    client: Optional["rubpy.BotClient"] = None

    @property
    def message_id(self) -> str:
        if self.new_message:
            return self.new_message.message_id
        if self.updated_message:
            return self.updated_message.message_id
        return None

    async def reply(
        self,
        text: str,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE,
        chat_id: str = None,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ) -> MessageId:
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_message(
            chat_id=chat_id or self.chat_id,
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            reply_to_message_id=(
                self.message_id
            ),
            chat_keypad_type=chat_keypad_type,
            parse_mode=parse_mode,
            metadata=metadata,
        )

    async def reply_file(
        self,
        file: Optional[str] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE,
        chat_id: str = None,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ) -> MessageId:
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
            reply_to_message_id=(
                self.message_id
            ),
            chat_keypad_type=chat_keypad_type,
            parse_mode=parse_mode,
            metadata=metadata,
        )

    async def reply_photo(
        self,
        file: Optional[str] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE,
        chat_id: str = None,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ) -> MessageId:
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_file(
            chat_id=chat_id or self.chat_id,
            file=file,
            file_id=file_id,
            text=text,
            type="Image",
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            reply_to_message_id=(
                self.message_id
            ),
            chat_keypad_type=chat_keypad_type,
            parse_mode=parse_mode,
            metadata=metadata,
        )

    async def reply_video(
        self,
        file: Optional[str] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE,
        chat_id: str = None,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ) -> MessageId:
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_file(
            chat_id=chat_id or self.chat_id,
            file=file,
            file_id=file_id,
            text=text,
            type="Video",
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            reply_to_message_id=(
                self.message_id
            ),
            chat_keypad_type=chat_keypad_type,
            parse_mode=parse_mode,
            metadata=metadata,
        )

    async def reply_voice(
        self,
        file: Optional[str] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE,
        chat_id: str = None,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ) -> MessageId:
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_file(
            chat_id=chat_id or self.chat_id,
            file=file,
            file_id=file_id,
            text=text,
            type="Voice",
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            reply_to_message_id=(
                self.message_id
            ),
            chat_keypad_type=chat_keypad_type,
            parse_mode=parse_mode,
            metadata=metadata,
        )

    async def reply_music(
        self,
        file: Optional[str] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE,
        chat_id: str = None,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ) -> MessageId:
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_file(
            chat_id=chat_id or self.chat_id,
            file=file,
            file_id=file_id,
            text=text,
            type="Music",
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            reply_to_message_id=(
                self.message_id
            ),
            chat_keypad_type=chat_keypad_type,
            parse_mode=parse_mode,
            metadata=metadata,
        )

    async def reply_gif(
        self,
        file: Optional[str] = None,
        file_id: Optional[str] = None,
        text: Optional[str] = None,
        chat_keypad: Optional[Keypad] = None,
        inline_keypad: Optional[Keypad] = None,
        disable_notification: bool = False,
        chat_keypad_type: ChatKeypadTypeEnum = ChatKeypadTypeEnum.NONE,
        chat_id: str = None,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ) -> MessageId:
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_file(
            chat_id=chat_id or self.chat_id,
            file=file,
            file_id=file_id,
            text=text,
            type="Gif",
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            reply_to_message_id=(
                self.message_id
            ),
            chat_keypad_type=chat_keypad_type,
            parse_mode=parse_mode,
            metadata=metadata,
        )

    async def delete(
        self, chat_id: Optional[str] = None, message_id: Optional[str] = None
    ):
        return await self.client.delete_message(
            chat_id or self.chat_id,
            message_id or self.message_id,
        )
    
    async def edit_keypad(self, chat_keypad: Optional["rubpy.bot.models.Keypad"] = None, message_id: Optional[str] = None):
        return await self.client.edit_chat_keypad(
            chat_id=self.chat_id,
            message_id=message_id or self.message_id,
            chat_keypad=chat_keypad,
        )

    async def download(
        self,
        file_id: Optional[str] = None,
        save_as: Optional[str] = None,
        progress: Optional[Callable[[int, int], None]] = None,
        chunk_size: int = 65536,
        as_bytes: bool = False,
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

        return await self.client.download_file(
            file_id=file_id or self.find_key("file_id"),
            save_as=save_as,
            progress=progress,
            chunk_size=chunk_size,
            as_bytes=as_bytes,
            file_name=self.find_key("file_name"),
        )


@dataclass
class InlineMessage(DictLike):
    sender_id: Optional[str] = None
    text: Optional[str] = None
    file: Optional[File] = None
    location: Optional[Location] = None
    aux_data: Optional[AuxData] = None
    message_id: Optional[str] = None
    chat_id: Optional[str] = None
    client: "rubpy.BotClient" = None

    async def edit_text(self, text: str, message_id: Optional[str] = None):
        return await self.client.edit_message_text(
            chat_id=self.chat_id,
            message_id=message_id or self.message_id,
            text=text,
        )
    
    async def edit_keypad(self, inline_keypad: Optional["rubpy.bot.models.Keypad"] = None, message_id: Optional[str] = None):
        return await self.client.edit_message_keypad(
            chat_id=self.chat_id,
            message_id=message_id or self.message_id,
            inline_keypad=inline_keypad,
        )

    async def reply(
        self,
        text: str,
        chat_keypad: Optional["rubpy.bot.models.Keypad"] = None,
        inline_keypad: Optional["rubpy.bot.models.Keypad"] = None,
        disable_notification: bool = False,
        chat_keypad_type: "rubpy.bot.enums.ChatKeypadTypeEnum" = ChatKeypadTypeEnum.NONE,
        chat_id: str = None,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ):
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_message(
            chat_id=chat_id or self.chat_id,
            text=text,
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type,
            parse_mode=parse_mode,
            metadata=metadata,
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
        chat_id: str = None,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
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
            chat_keypad_type=chat_keypad_type,
            parse_mode=parse_mode,
            metadata=metadata,
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
        chat_id: str = None,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ):
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_file(
            chat_id=chat_id or self.chat_id,
            file=file,
            file_id=file_id,
            text=text,
            type="Image",
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type,
            parse_mode=parse_mode,
            metadata=metadata,
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
        chat_id: str = None,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ):
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_file(
            chat_id=chat_id or self.chat_id,
            file=file,
            file_id=file_id,
            text=text,
            type="Image",
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type,
            parse_mode=parse_mode,
            metadata=metadata,
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
        chat_id: str = None,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ):
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_file(
            chat_id=chat_id or self.chat_id,
            file=file,
            file_id=file_id,
            text=text,
            type="Music",
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type,
            parse_mode=parse_mode,
            metadata=metadata,
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
        chat_id: str = None,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ):
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_file(
            chat_id=chat_id or self.chat_id,
            file=file,
            file_id=file_id,
            text=text,
            type="Gif",
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type,
            parse_mode=parse_mode,
            metadata=metadata,
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
        chat_id: str = None,
        parse_mode: Optional[Union[ParseMode, str]] = None,
        metadata: Optional[Metadata] = None,
    ):
        if not self.client:
            raise ValueError("Client not set for Update")
        return await self.client.send_file(
            chat_id=chat_id or self.chat_id,
            file=file,
            file_id=file_id,
            text=text,
            type="Video",
            chat_keypad=chat_keypad,
            inline_keypad=inline_keypad,
            disable_notification=disable_notification,
            chat_keypad_type=chat_keypad_type,
            parse_mode=parse_mode,
            metadata=metadata,
        )

    async def delete(
        self, chat_id: Optional[str] = None, message_id: Optional[str] = None
    ):
        return await self.client.delete_message(
            chat_id or self.chat_id, message_id or self.message_id
        )
