from pydantic import BaseModel
from typing import Literal


class ButtonSelectionItem(BaseModel):
    text: str
    image_url: str
    type: Literal['TextOnly', 'TextImgThu', 'TextImgBig']