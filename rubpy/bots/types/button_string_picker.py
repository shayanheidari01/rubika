from typing import List
from pydantic import BaseModel


class ButtonStringPicker(BaseModel):
    items: List[str]
    default_value: str
    title: str