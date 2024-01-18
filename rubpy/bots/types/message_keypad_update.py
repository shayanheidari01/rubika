from .keypad import Keypad
from pydantic import BaseModel


class MessageKeypadUpdate(BaseModel):
    message_id: str
    inline_keypad: Keypad