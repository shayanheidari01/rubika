
from dataclasses import dataclass, fields
from typing import List, Optional, Union

import rubpy
from .file import File
from .dict_like import DictLike
from ..enums import ForwardedFromType, LiveLocationStatus, PollStatusEnum


@dataclass
class Location(DictLike):
    longitude: Optional[str] = None
    latitude: Optional[str] = None

@dataclass
class AuxData(DictLike):
    start_id: Optional[str] = None
    button_id: Optional[str] = None

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
    poll_status: Optional[PollStatus] =None

@dataclass
class Sticker(DictLike):
    sticker_id: Optional[str] = None
    file: Optional[File] = None
    emoji_character: Optional[str] = None

@dataclass
class ContactMessage(DictLike):
    phone_number: Optional[str] = None
    first_name: Optional[File] = None
    last_name: Optional[str] = None

@dataclass
class ForwardedFrom(DictLike):
    type_from: Optional[ForwardedFromType] = None
    message_id: Optional[Union[int, str]] = None
    from_chat_id: Optional[str] = None
    from_sender_id: Optional[str] = None

@dataclass
class LiveLocation(DictLike):
    start_time: Optional[str] = None
    live_period: Optional[int] = None
    current_location: Optional[Location] = None
    user_id: Optional[str] = None
    status: Optional[LiveLocationStatus] = None
    last_update_time: Optional[str] = None

@dataclass
class MessageId(DictLike):
    message_id: Optional[str] = None
    new_message_id: Optional[str] = None
    file_id: Optional[str] = None
    chat_id: Optional[str] = None
    client: Optional["rubpy.BotClient"] = None

    async def delete(self):
        return await self.client.delete_message(self.chat_id, self.message_id or self.new_message_id)

    async def edit_text(self, new_text: str):
        return await self.client.edit_message_text(self.chat_id, self.message_id or self.new_message_id, new_text)


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