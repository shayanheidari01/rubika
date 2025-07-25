from dataclasses import dataclass
from typing import List, Optional
from rubpy.bot.models import Button

from .dict_like import DictLike


@dataclass
class KeypadRow(DictLike):
    buttons: List[Button]