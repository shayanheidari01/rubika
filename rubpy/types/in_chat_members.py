from typing import List, Optional
from pydantic import BaseModel
from .member import Member


class InChatMembers(BaseModel):
    in_chat_members: Optional[List[Member]]
    next_start_id: Optional[str] = None
    has_continue: Optional[bool] = None
    timestamp: Optional[str] = None