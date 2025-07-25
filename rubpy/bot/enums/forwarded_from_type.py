from enum import Enum

class ForwardedFromType(str, Enum):
    USER = 'User'
    CHANNEL = 'Channel'
    BOT = 'Bot'