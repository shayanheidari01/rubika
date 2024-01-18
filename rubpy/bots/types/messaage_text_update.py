from pydantic import BaseModel


class messageTextUpdate(BaseModel):
    message_id: str
    text: str