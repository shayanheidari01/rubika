from .add_channel import AddChannel
from .add_channel_members import AddChannelMembers
from .ban_channel_member import BanChannelMember
from .channel_preview_by_join_link import ChannelPreviewByJoinLink
from .check_channel_username import CheckChannelUsername
from .create_channel_voice_chat import CreateChannelVoiceChat
from .discard_channel_voice_chat import DiscardChannelVoiceChat
from .edit_channel_info import EditChannelInfo
from .get_banned_group_members import GetBannedGroupMembers
from .get_channel_admin_access_list import GetChannelAdminAccessList
from .get_channel_admin_members import GetChannelAdminMembers
from .get_channel_all_members import GetChannelAllMembers
from .get_channel_info import GetChannelInfo
from .get_channel_link import GetChannelLink
from .join_channel_action import JoinChannelAction
from .join_channel_by_link import JoinChannelByLink
from .remove_channel import RemoveChannel
from .set_channel_link import SetChannelLink
from .set_channel_voice_chat_setting import SetChannelVoiceChatSetting
from .update_channel_username import UpdateChannelUsername
from .seen_channel_messages import SeenChannelMessages


class Channels(
        AddChannel,
        AddChannelMembers,
        BanChannelMember,
        ChannelPreviewByJoinLink,
        CheckChannelUsername,
        CreateChannelVoiceChat,
        DiscardChannelVoiceChat,
        EditChannelInfo,
        GetBannedGroupMembers,
        GetChannelAdminAccessList,
        GetChannelAdminMembers,
        GetChannelAllMembers,
        GetChannelInfo,
        GetChannelLink,
        JoinChannelAction,
        JoinChannelByLink,
        RemoveChannel,
        SetChannelLink,
        SetChannelVoiceChatSetting,
        UpdateChannelUsername,
        SeenChannelMessages,
):
        pass