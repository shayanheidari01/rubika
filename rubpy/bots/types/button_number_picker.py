from pydantic import BaseModel
from typing import Union


class ButtonNumberPicker(BaseModel):
    min_value: int
    max_value: int
    default_value: Union[int, None]
    title: str