from typing import Optional, Literal
from pydantic import BaseModel
from .aux_data import AuxData
from .file import File
from .forwarded_from import ForwardedFrom
from .location import Location
from .sticker import Sticker
from contact_message import ContactMessage
from .poll import Poll
from .live_location import LiveLocation

class Message(BaseModel):
    message_id: str
    text: Optional[str]
    time: int
    is_edited: bool
    sender_type: Literal['User', 'Bot']
    sender_id: str

    aux_data: Optional[AuxData] = AuxData()
    file: Optional[File]
    reply_to_message_id: Optional[str]
    forwarded_from: Optional[ForwardedFrom]
    forwarded_no_link: Optional[str]
    location: Optional[Location]
    sticker: Optional[Sticker]
    contact_message: Optional[ContactMessage]
    poll: Optional[Poll]
    live_location: Optional[LiveLocation]