import sys
from importlib import util
from pathlib import Path

from .button import Button
from .keypad_row import KeypadRow
from .keypad import Keypad
from .chat import Chat

from .inline_message import InlineMessage
from .update import Update
from .file import File
from .bot import Bot
from .dict_like import DictLike
from .message import (
    Message,
    MessageId,
    ForwardedFrom,
    Location,
    AuxData,
    PollStatus,
    Poll,
    Sticker,
    ContactMessage,
    LiveLocation
)
from rubpy.bot.enums import ButtonTypeEnum

_LEGACY_MODULE_NAME = "rubpy.bot._models_impl"
_LEGACY_MODULE_PATH = Path(__file__).resolve().parent.parent / "models.py"


def _load_legacy_module():
    if _LEGACY_MODULE_NAME in sys.modules:
        return sys.modules[_LEGACY_MODULE_NAME]

    spec = util.spec_from_file_location(_LEGACY_MODULE_NAME, _LEGACY_MODULE_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load legacy models module at {_LEGACY_MODULE_PATH}")

    module = util.module_from_spec(spec)
    sys.modules[_LEGACY_MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module


_legacy = _load_legacy_module()

for _name in ("JoinChannelData", "ButtonLink", "OpenChatData"):
    globals()[_name] = getattr(_legacy, _name)


__all__ = sorted(
    {
        "AuxData",
        "Bot",
        "Button",
        "ButtonLink",
        "ButtonTypeEnum",
        "Chat",
        "ContactMessage",
        "DictLike",
        "File",
        "ForwardedFrom",
        "InlineMessage",
        "JoinChannelData",
        "Keypad",
        "KeypadRow",
        "LiveLocation",
        "Location",
        "Message",
        "MessageId",
        "OpenChatData",
        "Poll",
        "PollStatus",
        "Sticker",
        "Update",
    }
)