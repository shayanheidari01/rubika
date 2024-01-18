from typing import List
from pydantic import BaseModel
from .poll_status import PollStatus


class Poll(BaseModel):
    question: str
    options: List[str]
    poll_status: PollStatus