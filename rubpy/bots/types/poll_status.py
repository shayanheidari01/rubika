from typing import Literal, List
from pydantic import BaseModel


class PollStatus(BaseModel):
    state: Literal['Open', 'Closed']
    selection_index: int
    percent_vote_options: List[int]
    total_vote: int
    show_total_votes: bool