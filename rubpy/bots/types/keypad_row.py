from pydantic import BaseModel
from .button import Button
from typing import List

class KeypadRow(BaseModel):
    buttons: List[Button]