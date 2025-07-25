from enum import Enum


class ChatTypeEnum(str, Enum):
    USER = "User"
    GROUP = "Group"
    BOT = "Bot"
    CHANNEL = "Channel"