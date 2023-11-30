from pydantic import BaseModel
from typing import Optional, List

class OnlineTime(BaseModel):
    type: Optional[str] = None
    approximate_period: Optional[str] = None

class AvatarThumbnail(BaseModel):
    file_id: Optional[str] = None
    mime: Optional[str] = None
    dc_id: Optional[str] = None
    access_hash_rec: Optional[str] = None
    file_name: Optional[str] = None
    cdn_tag: Optional[str] = None

class WarningInfo(BaseModel):
    warning_id: Optional[str] = None
    title: Optional[str] = None
    text: Optional[str] = None
    link: Optional[dict] = None
    title_color: Optional[dict] = None

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
    warning_info: Optional[WarningInfo] = None

class DeleteContact(BaseModel):
    user: Optional[User] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class AddAddressBook(BaseModel):
    user: Optional[User] = None
    user_exist: Optional[bool] = None
    timestamp: Optional[str] = None
    can_receive_call: Optional[bool] = None
    can_video_call: Optional[bool] = None

class GetContacts(BaseModel):
    users: Optional[List[User]] = []
    next_start_id: Optional[str] = None
    has_continue: Optional[bool] = None
    state: Optional[int] = None
    timestamp: Optional[str] = None