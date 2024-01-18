from typing import Literal
from pydantic import BaseModel


class ForwardedFrom(BaseModel):
    type_from: Literal['User', 'Channel', 'Bot']
    message_id: str
    from_chat_id: str
    from_sender_id: str