from .delete_avatar import DeleteAvatar
from .delete_chat_history import DeleteChatHistory
from .get_abs_objects import GetAbsObjects
from .get_avatars import GetAvatars
from .get_chats import GetChats
from .get_chats_updates import GetChatsUpdates
from .get_link_from_app_url import GetLinkFromAppUrl
from .upload_avatar import UploadAvatar
from .set_action_chat import SetActionChat
from .send_chat_activity import SendChatActivity
from .seen_chats import SeenChats
from .search_chat_messages import SearchChatMessages


class Chats(
    DeleteAvatar,
    DeleteChatHistory,
    GetAbsObjects,
    GetAvatars,
    GetChats,
    GetChatsUpdates,
    GetLinkFromAppUrl,
    UploadAvatar,
    SetActionChat,
    SendChatActivity,
    SeenChats,
    SearchChatMessages,
):
    pass