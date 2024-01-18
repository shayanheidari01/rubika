from datetime import datetime
from .location import Location
from typing import Literal
from pydantic import BaseModel


class LiveLocation(BaseModel):
    start_time: datetime
    live_period: int  # In Second
    current_location: Location
    user_id: str
    status: Literal['Stopped', 'Live']
    last_update_time: datetime