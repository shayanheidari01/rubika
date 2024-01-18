from pydantic import BaseModel
from typing import Optional
from .online_time import OnlineTime
from .avatar_thumbnail import AvatarThumbnail


class Member(BaseModel):
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