from enum import Enum

class ChatAction(str, Enum):
    TYPING = 'Typing'
    "Typing text message"

    UPLOADING = 'Uploading'
    "Uploading photo"

    RECORD_AUDIO = 'Recording'
    "Recording audio"