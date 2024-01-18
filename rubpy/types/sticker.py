from pydantic import BaseModel
from typing import Optional
from .file import File


class Sticker(BaseModel):
    emoji_character: Optional[str] = None
    w_h_ratio: Optional[str] = None
    sticker_id: Optional[str] = None
    file: Optional[File] = None
    sticker_set_id: Optional[str] = None