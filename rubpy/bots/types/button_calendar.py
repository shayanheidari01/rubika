from pydantic import BaseModel
from typing import Literal


class ButtonCalendar(BaseModel):
    default_value: str
    type: Literal['DatePersian', 'DateGregorian']
    min_year: str
    max_year: str
    title: str