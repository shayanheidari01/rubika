import sys
from importlib import util
from pathlib import Path

from .button_type import ButtonTypeEnum
from .chat_keypad_type import ChatKeypadTypeEnum
from .update_type import UpdateTypeEnum
from .chat_type import ChatTypeEnum
from .forwarded_from_type import ForwardedFromType
from .payment_status import PaymentStatusEnum
from .live_location_status import LiveLocationStatus
from .poll_status import PollStatusEnum

_LEGACY_MODULE_NAME = "rubpy.bot._enums_impl"
_LEGACY_MODULE_PATH = Path(__file__).resolve().parent.parent / "enums.py"


def _load_legacy_module():
    if _LEGACY_MODULE_NAME in sys.modules:
        return sys.modules[_LEGACY_MODULE_NAME]

    spec = util.spec_from_file_location(_LEGACY_MODULE_NAME, _LEGACY_MODULE_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load legacy enums module at {_LEGACY_MODULE_PATH}")

    module = util.module_from_spec(spec)
    sys.modules[_LEGACY_MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


_legacy = _load_legacy_module()

for _name in (
    "STREnum",
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
):
    globals().setdefault(_name, getattr(_legacy, _name))


__all__ = sorted(
    {
        "ButtonTypeEnum",
        "ChatKeypadTypeEnum",
        "UpdateTypeEnum",
        "ChatTypeEnum",
        "ForwardedFromType",
        "PaymentStatusEnum",
        "LiveLocationStatus",
        "PollStatusEnum",
        "STREnum",
        "ForwardedFromEnum",
        "LiveLocationStatusEnum",
        "ButtonSelectionTypeEnum",
        "ButtonSelectionSearchEnum",
        "ButtonSelectionGetEnum",
        "ButtonCalendarTypeEnum",
        "ButtonTextboxTypeKeypadEnum",
        "ButtonTextboxTypeLineEnum",
        "ButtonLocationTypeEnum",
        "MessageSenderEnum",
        "UpdateEndpointTypeEnum",
        "ButtonLinkTypeEnum",
    }
)