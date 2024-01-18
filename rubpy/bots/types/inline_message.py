from pydantic import BaseModel
from typing import Optional
from .file import File
from .location import Location
from .aux_data import AuxData


class InlineMessage(BaseModel):
    sender_id: str
    text: str
    file: Optional[File]
    location: Optional[Location]
    aux_data: AuxData
    message_id: str
    chat_id: str