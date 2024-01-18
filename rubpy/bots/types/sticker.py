from pydantic import BaseModel
from .file import File


class Sticker(BaseModel):
    sticker_id: str
    file: File
    emoji_character: str