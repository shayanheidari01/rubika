from dataclasses import dataclass
from typing import Optional

from .dict_like import DictLike


@dataclass
class File(DictLike):
    file_id: Optional[str] = None
    file_name: Optional[str] = None  # یا هر فیلد دیگه که در مدل File داری
    size: Optional[str] = None