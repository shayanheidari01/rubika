from enum import Enum

class Access(str, Enum):
    ChangeInfo = "ChangeInfo"
    PinMessages = "PinMessages"
    DeleteGlobalAllMessages = "DeleteGlobalAllMessages"
    BanMember = "BanMember"
    SetAdmin = "SetAdmin"
    SetJoinLink = "SetJoinLink"
    SetMemberAccess = "SetMemberAccess"
    ViewMembers = "ViewMembers"
    ViewAdmins = "ViewAdmins"
    SendMessages = "SendMessages"
    AddMember = "AddMember"
    ViewInfo = "ViewInfo"
    ViewMessages = "ViewMessages"
    DeleteLocalMessages = "DeleteLocalMessages"
    EditMyMessages = "EditMyMessages"
    DeleteGlobalMyMessages = "DeleteGlobalMyMessages"