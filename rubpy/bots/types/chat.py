from typing import Literal
from pydantic import BaseModel


class Chat(BaseModel):
    chat_id: str
    chat_type: Literal['User', 'Bot', 'Group', 'Channel']
    user_id: str
    first_name: str
    last_name: str
    title: str
    username: str