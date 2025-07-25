from dataclasses import dataclass
from typing import Optional

from typing import Dict
from rubpy.bot.enums import ButtonTypeEnum
from .dict_like import DictLike


@dataclass
class Button(DictLike):
    id: Optional[str] = None
    type: Optional[ButtonTypeEnum] = None
    button_text: Optional[str] = None
    button_selection: Optional[Dict] = None
    button_calendar: Optional[Dict] = None
    button_number_picker: Optional[Dict] = None
    button_string_picker: Optional[Dict] = None
    button_location: Optional[Dict] = None
    button_textbox: Optional[Dict] = None