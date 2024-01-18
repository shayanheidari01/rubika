from pydantic import BaseModel


class File(BaseModel):
    file_id: str
    file_name: str
    size: str