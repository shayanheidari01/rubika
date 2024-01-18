from pydantic import BaseModel
from typing import Optional


class AuxData(BaseModel):
    start_id: Optional[str] = None
    button_id: Optional[str] = None