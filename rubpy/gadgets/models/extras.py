from pydantic import BaseModel, HttpUrl, Field, PositiveInt
from typing import Optional, List

class AvatarThumbnail(BaseModel):
    file_id: Optional[str] = None
    mime: Optional[str] = None
    dc_id: Optional[str] = None
    access_hash_rec: Optional[str] = None

class Object(BaseModel):
    object_guid: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str] = None
    avatar_thumbnail: Optional[AvatarThumbnail] = None
    is_verified: Optional[bool] = None
    is_deleted: Optional[bool] = None
    count_members: Optional[int] = None
    username: Optional[str] = None

class SearchGlobalObjects(BaseModel):
    objects: list[Object]
    has_continue: Optional[bool] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class OnlineTime(BaseModel):
    type: Optional[str] = None
    approximate_period: Optional[str] = None

class AvatarThumbnail(BaseModel):
    file_id: Optional[str] = None
    mime: Optional[str] = None
    dc_id: Optional[str] = None
    access_hash_rec: Optional[str] = None

class LastMessage(BaseModel):
    message_id: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    author_object_guid: Optional[str] = None
    is_mine: Optional[bool] = None
    author_type: Optional[str] = None

class AbsObject(BaseModel):
    object_guid: Optional[str] = None
    type: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_thumbnail: Optional[AvatarThumbnail] = None
    is_verified: Optional[bool] = None
    is_deleted: Optional[bool] = None

class Chat(BaseModel):
    object_guid: Optional[str] = None
    access: Optional[list[str]] = []
    count_unseen: Optional[int] = None
    is_mute: Optional[bool] = None
    is_pinned: Optional[bool] = None
    time_string: Optional[str] = None
    last_message: Optional[LastMessage] = None
    last_seen_my_mid: Optional[str] = None
    last_seen_peer_mid: Optional[str] = None
    status: Optional[str] = None
    time: Optional[int] = None
    abs_object: Optional[AbsObject] = None
    is_blocked: Optional[bool] = None
    last_message_id: Optional[str] = None
    last_deleted_mid: Optional[str] = None
    is_in_contact: Optional[bool] = None

class ChatReactionSetting(BaseModel):
    reaction_type: Optional[str] = Field(None, description="Type of reactions in chat")
    selected_reactions: Optional[List[str]] = Field(None, description="List of selected reactions in the chat")

class User(BaseModel):
    user_guid: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    avatar_thumbnail: Optional[AvatarThumbnail] = None
    last_online: Optional[int] = None
    bio: Optional[str] = None
    is_deleted: Optional[bool] = None
    is_verified: Optional[bool] = None
    online_time: Optional[OnlineTime] = None

class Channel(BaseModel):
    channel_guid: Optional[str] = Field(None, description="Channel ID")
    channel_title: Optional[str] = Field(None, description="Channel title")
    avatar_thumbnail: Optional[AvatarThumbnail] = Field(None, description="Profile image information")
    count_members: Optional[PositiveInt] = Field(None, description="Number of channel members")
    description: Optional[str] = Field(None, description="Channel description")
    username: Optional[str] = Field(None, description="Channel username")
    is_deleted: Optional[bool] = Field(None, description="Channel deletion status")
    is_verified: Optional[bool] = Field(None, description="Channel verification status")
    share_url: Optional[HttpUrl] = Field(None, description="Channel sharing URL")
    channel_type: Optional[str] = Field(None, description="Channel type")
    sign_messages: Optional[bool] = Field(None, description="Message signing capability status")
    chat_reaction_setting: Optional[ChatReactionSetting] = Field(None, description="Conversation reaction settings")

class GetObjectByUsername(BaseModel):
    exist: Optional[bool] = None
    type: Optional[str] = None
    user: Optional[User] = None
    channel: Optional[Channel] = None
    chat: Optional[Chat] = None
    timestamp: Optional[str] = None
    is_in_contact: Optional[bool] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class OpenChatData(BaseModel):
    object_guid: Optional[str] = None
    object_type: Optional[str] = None
    message_id: Optional[int] = None

class LinkData(BaseModel):
    type: Optional[str] = None
    link_url: Optional[str] = None
    open_chat_data: Optional[OpenChatData] = None

class GetLinkFromAppUrl(BaseModel):
    link: Optional[LinkData] = None

class ChatGuidType(BaseModel):
    type: Optional[str] = None
    object_guid: Optional[str] = None

class MessageInfo(BaseModel):
    message_id: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    is_mine: Optional[bool] = None

class ChatInfo(BaseModel):
    time_string: Optional[str] = None
    last_message: Optional[MessageInfo] = None
    time: Optional[int] = None
    last_message_id: Optional[str] = None
    group_voice_chat_id: Optional[str] = None

class ChatUpdate(BaseModel):
    object_guid: Optional[str] = None
    action: Optional[str] = None
    chat: Optional[ChatInfo] = None
    updated_parameters: Optional[list[str]] = None
    timestamp: Optional[str] = None
    type: Optional[str] = None

class PerformerData(BaseModel):
    type: Optional[str] = None
    object_guid: Optional[str] = None

class EventData(BaseModel):
    type: Optional[str] = None
    performer_object: Optional[PerformerData] = None

class MessageData(BaseModel):
    message_id: Optional[str] = None
    text: Optional[str] = None
    time: Optional[str] = None
    is_edited: Optional[bool] = None
    type: Optional[str] = None
    event_data: Optional[EventData] = None

class MessageUpdate(BaseModel):
    message_id: Optional[str] = None
    action: Optional[str] = None
    message: Optional[MessageData] = None
    updated_parameters: Optional[list[str]] = None
    timestamp: Optional[str] = None
    prev_message_id: Optional[str] = None
    object_guid: Optional[str] = None
    type: Optional[str] = None
    state: Optional[str] = None

class GroupVoiceChatData(BaseModel):
    voice_chat_id: Optional[str] = None
    state: Optional[str] = None
    join_muted: Optional[bool] = None
    participant_count: Optional[int] = None
    title: Optional[str] = None
    version: Optional[int] = None

class ChannelVoiceChatData(BaseModel):
    voice_chat_id: Optional[str] = None
    state: Optional[str] = None
    join_muted: Optional[bool] = None
    participant_count: Optional[int] = None
    title: Optional[str] = None
    version: Optional[int] = None

class GroupVoiceChatUpdate(BaseModel):
    voice_chat_id: Optional[str] = None
    group_guid: Optional[str] = None
    action: Optional[str] = None
    group_voice_chat: Optional[GroupVoiceChatData] = None
    updated_parameters: Optional[list[str]] = None
    timestamp: Optional[str] = None
    chat_guid_type: Optional[ChatGuidType] = None

class ChannelVoiceChatUpdate(BaseModel):
    voice_chat_id: Optional[str] = None
    channel_guid: Optional[str] = None
    action: Optional[str] = None
    channel_voice_chat: Optional[ChannelVoiceChatData] = None
    updated_parameters: Optional[list[str]] = None
    timestamp: Optional[str] = None
    chat_guid_type: Optional[ChatGuidType] = None

class ExistGroupVoiceChat(BaseModel):
    voice_chat_id: Optional[str] = None
    state: Optional[str] = None
    join_muted: Optional[bool] = None
    participant_count: Optional[int] = None
    title: Optional[str] = None
    version: Optional[int] = None

class ExistChannelVoiceChat(BaseModel):
    voice_chat_id: Optional[str] = None
    state: Optional[str] = None
    join_muted: Optional[bool] = None
    participant_count: Optional[int] = None
    title: Optional[str] = None
    version: Optional[int] = None

class CreateVoiceCall(BaseModel):
    status: Optional[str] = None
    chat_update: Optional[ChatUpdate] = None
    message_update: Optional[MessageUpdate] = None
    group_voice_chat_update: Optional[GroupVoiceChatUpdate] = None
    channel_voice_chat_update: Optional[ChannelVoiceChatUpdate] = None
    exist_group_voice_chat: Optional[ExistGroupVoiceChat] = None
    exist_channel_voice_chat: Optional[ExistChannelVoiceChat] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None
