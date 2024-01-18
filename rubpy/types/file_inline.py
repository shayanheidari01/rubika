from typing import Optional
from pydantic import BaseModel


class FileInline(BaseModel):
    file_id: Optional[int] = None
    mime: Optional[str] = None
    dc_id: Optional[int] = None
    access_hash_rec: Optional[str] = None
    file_name: Optional[str] = None
    thumb_inline: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    time: Optional[int] = None
    size: Optional[int] = None
    type: Optional[str] = None
    is_round: Optional[bool] = None
    music_performer: Optional[str] = None