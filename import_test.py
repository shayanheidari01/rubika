"""Utility script to validate rubpy imports."""

import importlib
import sys


def run_import(statement: str) -> None:
    """Execute an import statement and raise if it fails."""
    namespace = {}
    try:
        exec(statement, namespace)
        print(f"SUCCESS: {statement}")
    except Exception as exc:  # pragma: no cover - diagnostic only
        print(f"FAILED: {statement} -> {exc}", file=sys.stderr)
        raise


MODULES = [
    "rubpy",
    "rubpy.bot",
    "rubpy.bot.models",
    "rubpy.bot.enums",
    "rubpy.bot.filters",
    "rubpy.bot.exceptions",
    "rubpy.filters",
    "rubpy.enums",
    "rubpy.types",
    "rubpy.utils",
    "rubpy.exceptions",
    "rubpy.sync",
]

IMPORT_STATEMENTS = [
    "from rubpy import Client, BotClient, SQLiteSession, StringSession, Rubino, types, utils, filters, exceptions, enums, sync, bot",
    "from rubpy.bot import BotClient as BotClientAlias, filters as bot_filters, enums as bot_enums, models as bot_models, exceptions as bot_exceptions",
    "from rubpy.bot.models import (JoinChannelData, ButtonLink, OpenChatData, Button, KeypadRow, Keypad, Chat, InlineMessage, Message, MessageId, ForwardedFrom, Location, AuxData, PollStatus, Poll, Sticker, ContactMessage, LiveLocation, DictLike, ButtonTypeEnum)",
]


def main() -> None:
    for module_name in MODULES:
        importlib.import_module(module_name)
        print(f"SUCCESS: importlib.import_module('{module_name}')")

    for statement in IMPORT_STATEMENTS:
        run_import(statement)


if __name__ == "__main__":
    main()
