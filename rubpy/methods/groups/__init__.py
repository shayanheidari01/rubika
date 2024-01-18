from .add_group import AddGroup
from .add_group_members import AddGroupMembers
from .ban_group_member import BanGroupMember
from .create_group_voice_chat import CreateGroupVoiceChat
from .delete_no_access_group_chat import DeleteNoAccessGroupChat
from .edit_group_info import EditGroupInfo
from .get_banned_group_members import GetBannedGroupMembers
from .get_group_admin_access_list import GetGroupAdminAccessList
from .get_group_admin_members import GetGroupAdminMembers
from .get_group_all_members import GetGroupAllMembers
from .get_group_default_access import GetGroupDefaultAccess
from .get_group_info import GetGroupInfo
from .get_group_link import GetGroupLink
from .get_group_mention_list import GetGroupMentionList
from .get_group_voice_chat_updates import GetGroupVoiceChatUpdates
from .group_preview_by_join_link import GroupPreviewByJoinLink
from .join_group import JoinGroup
from .leave_group import LeaveGroup
from .leave_group_voice_chat import LeaveGroupVoiceChat
from .remove_group import RemoveGroup
from .set_group_admin import SetGroupAdmin
from .set_group_default_access import SetGroupDefaultAccess
from .set_group_link import SetGroupLink
from .set_group_voice_chat_setting import SetGroupVoiceChatSetting


class Groups(
    AddGroup,
    AddGroupMembers,
    BanGroupMember,
    CreateGroupVoiceChat,
    DeleteNoAccessGroupChat,
    EditGroupInfo,
    GetBannedGroupMembers,
    GetGroupAdminAccessList,
    GetGroupAdminMembers,
    GetGroupAllMembers,
    GetGroupDefaultAccess,
    GetGroupInfo,
    GetGroupLink,
    GetGroupMentionList,
    GetGroupVoiceChatUpdates,
    GroupPreviewByJoinLink,
    JoinGroup,
    LeaveGroup,
    LeaveGroupVoiceChat,
    RemoveGroup,
    SetGroupAdmin,
    SetGroupDefaultAccess,
    SetGroupLink,
    SetGroupVoiceChatSetting,
):
    pass