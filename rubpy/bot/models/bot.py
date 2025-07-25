from dataclasses import dataclass
from typing import Optional
from .file import File
from .dict_like import DictLike

@dataclass
class Bot(DictLike):
    bot_id: Optional[str] = None
    bot_title: Optional[str] = None
    description: Optional[str] = None
    username: Optional[str] = None
    start_message: Optional[str] = None
    share_url: Optional[str] = None
    avatar: Optional[File] = None
