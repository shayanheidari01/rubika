from pydantic import BaseModel
from typing import Optional, List, Dict, Union

class LastMessage(BaseModel):
    message_id: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    author_object_guid: Optional[str] = None
    is_mine: Optional[bool] = None
    author_title: Optional[str] = None
    author_type: Optional[str] = None

class ChatAccess(BaseModel):
    access: Optional[List[str]] = []
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
    abs_object: Optional[Dict] = None
    is_blocked: Optional[bool] = None
    last_message_id: Optional[str] = None
    last_deleted_mid: Optional[str] = None
    slow_mode_duration: Optional[int] = None
    group_my_last_send_time: Optional[int] = None
    pinned_message_ids: Optional[List[str]] = []

class ChatUpdate(BaseModel):
    object_guid: Optional[str] = None
    action: Optional[str] = None
    chat: Optional[ChatAccess] = None
    updated_parameters: Optional[List[str]] = None
    timestamp: Optional[str] = None
    type: Optional[str] = None

class LeaveGroup(BaseModel):
    chat_update: Optional[ChatUpdate] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class Group(BaseModel):
    group_guid: Optional[str] = None
    group_title: Optional[str] = None
    count_members: Optional[int] = None
    is_deleted: Optional[bool] = None
    is_verified: Optional[bool] = None
    slow_mode: Optional[int] = None
    chat_history_for_new_members: Optional[str] = None
    event_messages: Optional[bool] = None
    chat_reaction_setting: Optional[Union[str, Dict]] = None

class Chat(BaseModel):
    object_guid: Optional[str] = None
    action: Optional[str] = None
    access: Optional[List[str]] = None
    count_unseen: Optional[int] = None
    is_mute: Optional[bool] = None
    is_pinned: Optional[bool] = None
    time_string: Optional[str] = None
    last_message: Optional[Dict] = None
    last_seen_my_mid: Optional[str] = None
    last_seen_peer_mid: Optional[str] = None
    status: Optional[str] = None
    time: Optional[int] = None
    abs_object: Optional[Dict] = None
    is_blocked: Optional[bool] = None
    last_message_id: Optional[str] = None
    last_deleted_mid: Optional[str] = None
    slow_mode_duration: Optional[int] = None

class MessageUpdate(BaseModel):
    message_id: Optional[str] = None
    action: Optional[str] = None
    message: Optional[Dict] = None
    updated_parameters: Optional[List[str]] = None
    timestamp: Optional[str] = None
    prev_message_id: Optional[str] = None
    object_guid: Optional[str] = None
    type: Optional[str] = None
    state: Optional[str] = None

class JoinGroup(BaseModel):
    group: Optional[Group] = None
    is_valid: Optional[bool] = None
    chat_update: Optional[Chat] = None
    message_update: Optional[MessageUpdate] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class AddGroup(BaseModel):
    group: Optional[Group] = None
    chat_update: Optional[Chat] = None
    message_update: Optional[MessageUpdate] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class RemoveGroup(BaseModel):
    chat_update: Optional[Chat] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class GetGroupInfo(BaseModel):
    group: Optional[Group] = None
    chat: Optional[Chat] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None
    message_update: Optional[MessageUpdate] = None

class GroupLink(BaseModel):
    join_link: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class EditGroupInfo(BaseModel):
    group: Optional[Group] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class OnlineTime(BaseModel):
    type: Optional[str] = None
    approximate_period: Optional[str] = None

class InChatMemberList(BaseModel):
    member_type: Optional[str] = None
    member_guid: Optional[str] = None
    first_name: Optional[str] = None
    is_verified: Optional[bool] = None
    is_deleted: Optional[bool] = None
    promoted_by_object_guid: Optional[str] = None
    promoted_by_object_type: Optional[str] = None
    join_type: Optional[str] = None
    online_time: Optional[OnlineTime] = None

class InChatMember(BaseModel):
    in_chat_member: Optional[InChatMemberList] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class BanGroupMember(BaseModel):
    group: Optional[Group] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[Dict] = None

class AvatarThumbnail(BaseModel):
    file_id: Optional[str] = None
    mime: Optional[str] = None
    dc_id: Optional[str] = None
    access_hash_rec: Optional[str] = None

class AddedInChatMember(BaseModel):
    member_type: Optional[str] = None
    member_guid: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_thumbnail: Optional[AvatarThumbnail] = None
    is_verified: Optional[bool] = None
    is_deleted: Optional[bool] = None
    last_online: Optional[int] = None
    join_type: Optional[str] = None
    username: Optional[str] = None
    online_time: Optional[OnlineTime] = None

class AddGroupMembers(BaseModel):
    chat_update: Optional[ChatUpdate] = None
    message_update: Optional[MessageUpdate] = None
    added_in_chat_members: Optional[List[AddedInChatMember]] = None
    timestamp: Optional[str] = None
    group: Optional[Group] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class InChatGroupMember(BaseModel):
    member_type: Optional[str] = None
    member_guid: Optional[str] = None
    first_name: Optional[str] = None
    is_verified: Optional[bool] = None
    is_deleted: Optional[bool] = None
    last_online: Optional[int] = None
    join_type: Optional[str] = None
    online_time: Optional[OnlineTime] = None
    promoted_by_object_guid: Optional[str] = None
    promoted_by_object_type: Optional[str] = None
    removed_by_object_guid: Optional[str] = None
    removed_by_object_type: Optional[str] = None

class GetAllGroupMembers(BaseModel):
    in_chat_members: Optional[List[InChatGroupMember]] = None
    next_start_id: Optional[str] = None
    has_continue: Optional[bool] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class GetGroupAdminMembers(BaseModel):
    in_chat_members: Optional[List[InChatGroupMember]] = None
    next_start_id: Optional[str] = None
    has_continue: Optional[bool] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class GetGroupMentionList(BaseModel):
    in_chat_members: Optional[List[InChatGroupMember]] = None
    next_start_id: Optional[str] = None
    has_continue: Optional[bool] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class GetGroupDefaultAccess(BaseModel):
    access_list: Optional[List] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class OnlineTime(BaseModel):
    type: Optional[str] = None
    approximate_period: Optional[str] = None

class TopParticipants(BaseModel):
    member_type: Optional[str] = None
    member_guid: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_thumbnail: Optional[AvatarThumbnail] = None
    is_verified: Optional[bool] = None
    is_deleted: Optional[bool] = None
    username: Optional[str] = None
    online_time: Optional[OnlineTime] = None

class GroupPreviewByJoinLink(BaseModel):
    is_valid: Optional[bool] = None
    group: Optional[Group] = None
    has_joined: Optional[bool] = None
    top_participants: Optional[List[TopParticipants]] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class DeleteNoAccessGroupChat(BaseModel):
    chat_update: Optional[ChatUpdate] = None
    status: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class GetGroupAdminAccessList(BaseModel):
    access_list: Optional[List] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class GetBannedGroupMembers(BaseModel):
    in_chat_members: Optional[List[InChatGroupMember]] = []
    next_start_id: Optional[str] = None
    has_continue: Optional[bool] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None