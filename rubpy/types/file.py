from typing import Optional
from pydantic import BaseModel


class File(BaseModel):
    file_id: Optional[str] = None
    mime: Optional[str] = None
    dc_id: Optional[str] = None
    access_hash_rec: Optional[str] = None
    file_name: Optional[str] = None
    cdn_tag: Optional[str] = None