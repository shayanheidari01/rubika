from datetime import datetime
from pydantic import BaseModel
from .file import File

class Bot(BaseModel):
    bot_id: str
    bot_title: str
    avatar: File
    description: str
    username: str
    start_message: datetime
    share_url: str