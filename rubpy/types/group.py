from pydantic import BaseModel
from typing import Optional
from .avatar_thumbnail import AvatarThumbnail
from .chat_reaction_setting import ChatReactionSetting


class Group(BaseModel):
    group_guid: str
    group_title: str
    avatar_thumbnail: Optional[AvatarThumbnail] = None
    count_members: int
    is_deleted: bool
    is_verified: bool
    slow_mode: int
    chat_history_for_new_members: str
    event_messages: bool
    chat_reaction_setting: Optional[ChatReactionSetting] = None