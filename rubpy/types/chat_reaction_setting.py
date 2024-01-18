from pydantic import BaseModel
from typing import Optional

class ChatReactionSetting(BaseModel):
    reaction_type: Optional[str] = None