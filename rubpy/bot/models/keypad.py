from dataclasses import dataclass
from typing import List
from rubpy.bot.models import KeypadRow

from .dict_like import DictLike


@dataclass
class Keypad(DictLike):
    rows: List[KeypadRow]
    resize_keyboard: bool = True
    on_time_keyboard: bool = False
