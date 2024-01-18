from typing import Optional
from pydantic import BaseModel
from .sticker import Sticker
from .file_inline import FileInline


class Message(BaseModel):
    message_id: Optional[str] = None
    text: Optional[str] = None
    time: Optional[str] = None
    is_edited: Optional[bool] = None
    type: Optional[str] = None
    author_type: Optional[str] = None
    author_object_guid: Optional[str] = None
    sticker: Optional[Sticker] = None
    file_inline: Optional[FileInline] = None