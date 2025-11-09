from enum import Enum

class STREnum(str, Enum):
    pass

class ChatTypeEnum(STREnum):
    USER = "User"
    BOT = "Bot"
    GROUP = "Group"
    CHANNEL = "Channel"

class ForwardedFromEnum(STREnum):
    USER = "User"
    CHANNEL = "Channel"
    BOT = "Bot"

class PaymentStatusEnum(STREnum):
    Paid = "Paid"
    NotPaid = "NotPaid"

class PollStatusEnum(STREnum):
    OPEN = "Open"
    CLOSED = "Closed"

class LiveLocationStatusEnum(STREnum):
    STOPPED = "Stopped"
    LIVE = "Live"

class ButtonSelectionTypeEnum(STREnum):
    TextOnly = "TextOnly"
    TextImgThu = "TextImgThu"
    TextImgBig = "TextImgBig"

class ButtonSelectionSearchEnum(STREnum):
    NONE = "None"
    Local = "Local"
    Api = "Api"

class ButtonSelectionGetEnum(STREnum):
    Local = "Local"
    Api = "Api"

class ButtonCalendarTypeEnum(STREnum):
    DatePersian = "DatePersian"
    DateGregorian = "DateGregorian"

class ButtonTextboxTypeKeypadEnum(STREnum):
    STRING = "String"
    NUMBER = "Number"

class ButtonTextboxTypeLineEnum(STREnum):
    SingleLine = "SingleLine"
    MultiLine = "MultiLine"

class ButtonLocationTypeEnum(STREnum):
    PICKER = "Picker"
    VIEW = "View"

class ButtonTypeEnum(STREnum):
    SIMPLE = "Simple"
    SELECTION = "Selection"
    CALENDAR = "Calendar"
    NumberPicker = "NumberPicker"
    StringPicker = "StringPicker"
    LOCATION = "Location"
    PAYMENT = "Payment"
    CameraImage = "CameraImage"
    CameraVideo = "CameraVideo"
    GalleryImage = "GalleryImage"
    GalleryVideo = "GalleryVideo"
    FILE = "File"
    AUDIO = "Audio"
    RecordAudio = "RecordAudio"
    MyPhoneNumber = "MyPhoneNumber"
    MyLocation = "MyLocation"
    Textbox = "Textbox"
    LINK = "Link"
    AskMyPhoneNumber = "AskMyPhoneNumber"
    AskLocation = "AskLocation"
    BARCODE = "Barcode"

class ButtonLinkTypeEnum(STREnum):
    URL = "url"
    JoinChannel = "joinchannel"

class MessageSenderEnum(STREnum):
    USER = "User"
    BOT = "Bot"

class UpdateTypeEnum(STREnum):
    UpdatedMessage = "UpdatedMessage"
    NewMessage = "NewMessage"
    RemovedMessage = "RemovedMessage"
    StartedBot = "StartedBot"
    StoppedBot = "StoppedBot"
    UpdatedPayment = "UpdatedPayment"

class ChatKeypadTypeEnum(STREnum):
    NONE = "None"
    NEW = "New"
    REMOVE = "Remove"

class UpdateEndpointTypeEnum(STREnum):
    ReceiveUpdate = "ReceiveUpdate"
    ReceiveInlineMessage = "ReceiveInlineMessage"
    ReceiveQuery = "ReceiveQuery"
    GetSelectionItem = "GetSelectionItem"
    SearchSelectionItems = "SearchSelectionItems"

__all__ = [
    "ChatTypeEnum",
    "ForwardedFromEnum",
    "PaymentStatusEnum",
    "PollStatusEnum",
    "LiveLocationStatusEnum",
    "ButtonSelectionTypeEnum",
    "ButtonSelectionSearchEnum",
    "ButtonSelectionGetEnum",
    "ButtonCalendarTypeEnum",
    "ButtonTextboxTypeKeypadEnum",
    "ButtonTextboxTypeLineEnum",
    "ButtonLocationTypeEnum",
    "ButtonTypeEnum",
    "MessageSenderEnum",
    "UpdateTypeEnum",
    "ChatKeypadTypeEnum",
    "UpdateEndpointTypeEnum",
    "ButtonLinkTypeEnum",
    "STREnum"
]