from typing import Literal
from pydantic import BaseModel


class ButtonTextbox(BaseModel):
    type_line: Literal['SingleLine', 'MultiLine']
    type_keypad: Literal['String', 'Number']
    place_holder: str
    title: str
    default_value: str