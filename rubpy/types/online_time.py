from typing import Optional
from pydantic import BaseModel


class OnlineTime(BaseModel):
    type: Optional[str] = None
    exact_time: Optional[int] = None