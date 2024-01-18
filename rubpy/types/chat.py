from typing import Optional, List
from pydantic import BaseModel
from .message import Message
from .abs_object import AbsObject


class Chat(BaseModel):
    object_guid: Optional[str] = None
    access: Optional[List[str]] = None
    count_unseen: Optional[int] = None
    is_mute: Optional[bool] = None
    is_pinned: Optional[bool] = None
    time_string: Optional[str] = None
    last_message: Optional[Message] = None
    last_seen_my_mid: Optional[str] = None
    last_seen_peer_mid: Optional[str] = None
    status: Optional[str] = None
    time: Optional[int] = None
    abs_object: Optional[AbsObject] = None
    is_blocked: Optional[bool] = None
    last_message_id: Optional[str] = None
    last_deleted_mid: Optional[str] = None
    is_in_contact: Optional[bool] = None