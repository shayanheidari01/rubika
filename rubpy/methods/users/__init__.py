from .get_user_info import GetUserInfo
from .get_me import GetMe
from .set_block_user import SetBlockUser
from .delete_user_chat import DeleteUserChat
from .check_user_username import CheckUserUsername


class Users(
    GetUserInfo,
    GetMe,
    SetBlockUser,
    DeleteUserChat,
    CheckUserUsername,
):
    pass