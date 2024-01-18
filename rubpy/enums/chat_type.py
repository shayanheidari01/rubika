class ChatType:
    """Chat type enumeration used in :obj:`~pyrogram.types.Chat`."""

    PRIVATE = 'Private'
    "Chat is a private chat with a user"

    BOT = 'Bot'
    "Chat is a private chat with a bot"

    GROUP = 'Group'
    "Chat is a basic group"

    CHANNEL = 'Channel'
    "Chat is a channel"

    SERVICE = 'Service'
    "Chat is a service"