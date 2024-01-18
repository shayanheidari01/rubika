from typing import Optional, List
from pydantic import BaseModel
from .keypad_row import KeypadRow


class Keypad(BaseModel):
    rows: List[KeypadRow]
    resize_keyboard: Optional[bool]
    on_time_keyboard: Optional[bool]