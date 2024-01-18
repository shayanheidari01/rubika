from pydantic import BaseModel
from .chat import Chat

class ChatUpdate(BaseModel):
    object_guid: str
    action: str
    chat: Chat