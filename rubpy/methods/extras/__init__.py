from .get_object_by_username import GetObjectByUsername
from .search_global_objects import SearchGlobalObjects
from .get_profile_link_items import GetProfileLinkItems
from .ban_member import BanMember
from .get_info import GetInfo
from .join import Join
from .get_related_objects import GetRelatedObjects
from .get_transcription import GetTranscription
from .user_is_admin import UserIsAdmin
from .report_object import ReportObject
from.transcribe_voice import TranscribeVoice
from .get_join_links import GetJoinLinks
from .create_join_link import CreateJoinLink
from .get_join_requests import GetJoinRequests
from .action_on_join_request import ActionOnJoinRequest

class Exctras(
    GetObjectByUsername,
    SearchGlobalObjects,
    GetProfileLinkItems,
    BanMember,
    GetInfo,
    Join,
    GetRelatedObjects,
    GetTranscription,
    UserIsAdmin,
    ReportObject,
    TranscribeVoice,
    GetJoinLinks,
    CreateJoinLink,
    ActionOnJoinRequest,
    GetJoinRequests,
):
    pass