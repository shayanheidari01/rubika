from enum import Enum

class PollStatusEnum(str, Enum):
    OPEN = 'Open'
    CLOSED = 'Closed'