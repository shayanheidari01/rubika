from pydantic import BaseModel
from typing import List, Optional

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

class AbsObject(BaseModel):
    object_guid: Optional[str] = None
    type: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_verified: Optional[bool] = None
    is_deleted: Optional[bool] = None

class Chat(BaseModel):
    object_guid: Optional[str] = None
    access: Optional[List[str]] = None
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

class UserInfo(BaseModel):
    user_guid: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    last_online: Optional[int] = None
    bio: Optional[str] = None
    is_deleted: Optional[bool] = None
    is_verified: Optional[bool] = None
    online_time: Optional[OnlineTime] = None

class GetUserInfo(BaseModel):
    user: Optional[UserInfo] = None
    chat: Optional[Chat] = None
    timestamp: Optional[str] = None
    can_receive_call: Optional[bool] = None
    can_video_call: Optional[bool] = None

class ChatAccess(BaseModel):
    access: Optional[list[str]] = None
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
    abs_object: Optional[AbsObject] = None
    is_blocked: Optional[bool] = None
    last_message_id: Optional[str] = None
    last_deleted_mid: Optional[str] = None
    slow_mode_duration: Optional[int] = None
    group_my_last_send_time: Optional[int] = None
    pinned_message_ids: Optional[list[str]] = None

class ChatUpdate(BaseModel):
    object_guid: Optional[str] = None
    action: Optional[str] = None
    chat: Optional[ChatAccess] = None
    updated_parameters: Optional[list[str]] = None
    timestamp: Optional[str] = None
    type: Optional[str] = None

class BlockUser(BaseModel):
    chat_update: Optional[ChatUpdate] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class DeleteUserChat(BaseModel):
    chat_update: Optional[ChatUpdate] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class CheckUserName(BaseModel):
    exist: Optional[bool] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None
