from pydantic import BaseModel
from typing import Optional

class AvatarThumbnail(BaseModel):
    file_id: Optional[str] = None
    mime: Optional[str] = None
    dc_id: Optional[str] = None
    access_hash_rec: Optional[str] = None

class OnlineTime(BaseModel):
    type: Optional[str] = None
    exact_time: Optional[int] = None

class LastMessage(BaseModel):
    message_id: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    author_object_guid: Optional[str] = None
    is_mine: Optional[bool] = None
    author_title: Optional[str] = None
    author_type: Optional[str] = None

class ChatInfo(BaseModel):
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

class UserInfo(BaseModel):
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

class AvatarData(BaseModel):
    avatar_id: Optional[str] = None
    thumbnail: Optional[AvatarThumbnail] = None
    main: Optional[AvatarThumbnail] = None
    create_time: Optional[int] = None

class GetAvatars(BaseModel):
    avatars: Optional[list[AvatarData]] = []
    _client: Optional[str] = None
    original_update: Optional[str] = None

class ChatAccess(BaseModel):
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
    pinned_message_id: Optional[str] = None
    abs_object: Optional[dict] = None
    is_blocked: Optional[bool] = None
    last_message_id: Optional[str] = None
    last_deleted_mid: Optional[str] = None
    slow_mode_duration: Optional[int] = None
    group_my_last_send_time: Optional[int] = None
    pinned_message_ids: Optional[list[str]] = []

class ChatUpdate(BaseModel):
    object_guid: Optional[str] = None
    action: Optional[str] = None
    chat: Optional[ChatAccess] = None
    updated_parameters: Optional[list[str]] = []
    timestamp: Optional[str] = None
    type: Optional[str] = None

class DeleteAvatar(BaseModel):
    user: Optional[UserInfo] = None
    chat_update: Optional[ChatUpdate] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class GetChats(BaseModel):
    chats: Optional[list[ChatInfo]] = []
    next_start_id: Optional[str] = None
    state: Optional[int] = None
    has_continue: Optional[bool] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class SeenChats(BaseModel):
    chat_updates: Optional[list[ChatUpdate]] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class SetActionChat(BaseModel):
    chat_update: Optional[ChatUpdate] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class GetChatsUpdates(BaseModel):
    chats: list[ChatInfo]
    new_state: Optional[int] = None
    status: Optional[str] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class SendChatActivity(BaseModel):
    _client: Optional[str] = None
    original_update: Optional[str] = None

class DeleteChatHistory(BaseModel):
    chat_update: Optional[ChatUpdate] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class SearchChatMessages(BaseModel):
    message_ids: list[str]
    _client: Optional[str] = None
    original_update: Optional[str] = None
