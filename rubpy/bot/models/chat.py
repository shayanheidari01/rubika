from dataclasses import dataclass
from typing import Optional

from rubpy.bot.enums.chat_type import ChatTypeEnum
from .dict_like import DictLike


@dataclass
class Chat(DictLike):
    chat_id: Optional[str] = None
    chat_type: Optional[ChatTypeEnum] = None
    user_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    title: Optional[str] = None
    username: Optional[str] = None
