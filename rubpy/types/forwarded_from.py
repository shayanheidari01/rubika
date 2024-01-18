from typing import Optional
from pydantic import BaseModel


class ForwardedFrom(BaseModel):
    type_from: Optional[str] = None
    message_id: Optional[str] = None
    object_guid: Optional[str] = None