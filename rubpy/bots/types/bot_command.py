from pydantic import BaseModel

class BotCommand(BaseModel):
    command: str
    description: str