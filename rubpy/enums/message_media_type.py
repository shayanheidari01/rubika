from enum import Enum

class MessageMediaType(str, Enum):
    """Message media type"""

    AUDIO = 'Music'
    "Music media"

    MUSIC = 'Music'
    "Music media"

    DOCUMENT = 'File'
    "Document media"

    PHOTO = 'Image'
    "Photo media"

    STICKER = 'Sticker'
    "Sticker media"

    VIDEO = 'Video'
    "Video media"

    VOICE = 'Voice'
    "Voice media"

    CONTACT = 'Contact'
    "Contact media"

    LOCATION = 'Location'
    "Location media"

    POLL = 'Poll'
    "Poll media"

    GIF = 'Gif'
    "Gif media"