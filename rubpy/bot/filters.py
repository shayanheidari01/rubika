# Filters
import asyncio
import logging
import mimetypes
import re
from typing import Any, Dict, List, Optional, Union

from rubpy.bot.models import Update
from rubpy.bot.models import InlineMessage

logger = logging.getLogger(__name__)


def maybe_instance(f):
    return f() if isinstance(f, type) else f


class FilterMeta(type):
    def __and__(cls, other):
        return AndFilter(maybe_instance(cls), maybe_instance(other))

    def __rand__(cls, other):
        return AndFilter(maybe_instance(other), maybe_instance(cls))

    def __or__(cls, other):
        return OrFilter(maybe_instance(cls), maybe_instance(other))

    def __ror__(cls, other):
        return OrFilter(maybe_instance(other), maybe_instance(cls))

    def __invert__(cls):
        return NotFilter(maybe_instance(cls))


class Filter(metaclass=FilterMeta):
    async def check(self, update):
        raise NotImplementedError

    def __and__(self, other):
        return AndFilter(maybe_instance(self), maybe_instance(other))

    def __rand__(self, other):
        return AndFilter(maybe_instance(other), maybe_instance(self))

    def __or__(self, other):
        return OrFilter(maybe_instance(self), maybe_instance(other))

    def __ror__(self, other):
        return OrFilter(maybe_instance(other), maybe_instance(self))

    def __invert__(self):
        instance = self() if isinstance(self, type) else self
        return NotFilter(instance)


class AndFilter(Filter):
    def __init__(self, *filters: Filter):
        self.filters = filters

    async def check(self, update: Union["Update", "InlineMessage"]) -> bool:
        for f in self.filters:
            if isinstance(f, type):  # اگر کلاس دادیم
                f = f()
            if not await f.check(update):
                return False
        return True


class OrFilter(Filter):
    def __init__(self, *filters: Filter):
        self.filters = filters

    async def check(self, update):
        for f in self.filters:
            if isinstance(f, type):
                f = f()
            if await f.check(update):
                return True
        return False


class NotFilter(Filter):
    def __init__(self, f: Filter):
        self.f = f if not isinstance(f, type) else f()

    async def check(self, update):
        return not await self.f.check(update)


class text(Filter):
    """
    Filter for checking message text content.

    This filter can match messages based on:
    - An exact string match.
    - A regular expression pattern.
    - Or, if no value is given, it simply checks that the message has any text.

    Args:
        text (str, optional): The exact text or regex pattern to match.
        regex (bool): If True, `text` is treated as a regular expression.

    Returns:
        bool: True if the message text matches the given criteria.

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot.filters import text
        >>>
        >>> bot = BotClient("your_auth_token")
        >>>
        >>> # Match any text message
        >>> @bot.on_update(text)
        ... async def any_text(c, update):
        ...     await c.send_message(update.chat_id, "You sent some text!")
        >>>
        >>> # Match exact text
        >>> @bot.on_update(text("hello"))
        ... async def exact_match(c, update):
        ...     await c.send_message(update.chat_id, "You said hello!")
        >>>
        >>> # Match using regex
        >>> @bot.on_update(text(r"^/start.*", regex=True))
        ... async def regex_match(c, update):
        ...     await c.send_message(update.chat_id, "Start command detected!")
    """

    def __init__(self, text: Optional[str] = None, regex: bool = False):
        self.text = text
        self.regex = regex
        self._compiled = re.compile(text) if regex and text else None

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        try:
            text = update.find_key("text")
        except KeyError:
            return False
            
        if not text:
            return False

        if not self.text:
            return True

        if self.regex:
            return bool(self._compiled.match(text))

        return text == self.text


class commands(Filter):
    """
    Advanced filter for detecting bot commands (e.g. /start, !help, test).

    Features:
        - Supports multiple command prefixes (default: / and !).
        - Case-insensitive option.
        - Matches both exact commands and commands with arguments.
        - Supports single or multiple commands.

    Args:
        commands (Union[str, List[str]]): Command or list of commands (without prefix).
        prefixes (List[str], optional): Allowed prefixes (default: ["/", "!"]).
        case_sensitive (bool, optional): Whether command matching is case-sensitive. Default False.
        allow_no_prefix (bool, optional): If True, matches commands even without prefix. Default False.

    Example:
        >>> @bot.on_update(commands("start"))
        ... async def handle_start(c, update):
        ...     await update.reply("Welcome to the bot!")

        >>> @bot.on_update(commands(["help", "about"], prefixes=["/", ".", "!"]))
        ... async def handle_help(c, update):
        ...     await update.reply("Help/About detected!")

        >>> @bot.on_update(commands("test", allow_no_prefix=True))
        ... async def handle_test(c, update):
        ...     await update.reply("Matched with or without prefix")
    """

    def __init__(
        self,
        commands: Union[str, List[str]],
        prefixes: List[str] = ["/"],
        case_sensitive: bool = False,
        allow_no_prefix: bool = False,
    ):
        self.commands = [commands] if isinstance(commands, str) else commands
        self.prefixes = prefixes
        self.case_sensitive = case_sensitive
        self.allow_no_prefix = allow_no_prefix

        if not case_sensitive:
            self.commands = [cmd.lower() for cmd in self.commands]

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        text = (
            update.new_message.text
            if isinstance(update, Update) and update.new_message
            else update.text if isinstance(update, InlineMessage) else ""
        )
        if not text:
            return False

        # prepare text for matching
        check_text = text if self.case_sensitive else text.lower()

        # split into command + args
        parts = check_text.split(maxsplit=1)
        command_part = parts[0]

        # check with prefixes
        for cmd in self.commands:
            for prefix in self.prefixes:
                if command_part == f"{prefix}{cmd}" or command_part.startswith(
                    f"{prefix}{cmd}"
                ):
                    return True

            # allow matching without prefix
            if self.allow_no_prefix and (
                command_part == cmd or command_part.startswith(cmd)
            ):
                return True

        return False


class update_type(Filter):
    """
    Filter for matching specific update types.

    This filter checks if the update's type matches one or more given update types.
    It supports both `Update` objects (checking their `type` attribute)
    and `InlineMessage` objects (matched by the string `"InlineMessage"`).

    Args:
        update_types (Union[str, List[str]]): A single update type string or a list of update type strings.

    Returns:
        bool: True if the update's type matches one of the specified types.

    Example:
        >>> from rubpy import BotClient
        >>> from your_module import update_type
        >>>
        >>> bot = BotClient("your_auth_token")
        >>>
        >>> # Match only message updates
        >>> @bot.on_update(update_type("NewMessage"))
        ... async def handle_message_update(c, update):
        ...     await c.send_message(update.chat_id, "Received a message update.")
        >>>
        >>> # Match multiple types including inline messages
        >>> @bot.on_update(update_type(["NewMessage", "UpdatedMessage", "InlineMessage"]))
        ... async def handle_multiple_types(c, update):
        ...     await c.send_message(update.chat_id, "Received one of several update types.")
    """

    def __init__(self, update_types: Union[str, List[str]]):
        self.update_types = (
            [update_types] if isinstance(update_types, str) else update_types
        )

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        result = (isinstance(update, Update) and update.type in self.update_types) or (
            isinstance(update, InlineMessage) and "InlineMessage" in self.update_types
        )
        logger.debug(f"UpdateTypeFilter check: types={self.update_types}, update.type={update.type if isinstance(update, Update) else 'InlineMessage'}, result={result}")
        return result


class private(Filter):
    """
    Filter for detecting messages sent in private (one-on-one) chats.

    This filter checks whether the sender of the message is a regular user (i.e., not a group or bot).
    It's typically used to ensure that a handler only runs for messages from private chats.

    Returns:
        bool: True if the message was sent by a user in a private chat, otherwise False.

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot.models import Update
        >>> from rubpy.bot.filters import private
        >>>
        >>> bot_client = BotClient("your_bot_token")
        >>>
        >>> @bot_client.on_update(private)
        ... async def handle_private_message(c, update):
        ...     await c.send_message(update.chat_id, "You are chatting privately with the bot.")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        return bool(update.chat_id.startswith("b0"))


class group(Filter):
    """
    Filter for detecting messages sent from groups.

    This filter checks whether the sender of the message is of type `'Group'`.
    It's useful when you want a handler to be triggered only for messages
    originating from group chats.

    Returns:
        bool: True if the message was sent from a group, otherwise False.

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot.models import Update
        >>> from rubpy.bot.filters import group
        >>>
        >>> bot_client = BotClient("your_bot_token")
        >>>
        >>> @bot_client.on_update(group)
        ... async def handle_group_messages(c, update):
        ...     await c.send_message(update.chat_id, "This message came from a group!")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        return bool(update.chat_id.startswith("g0"))


class channel(Filter):
    """
    Filter for detecting messages sent from groups.

    This filter checks whether the sender of the message is of type `'Group'`.
    It's useful when you want a handler to be triggered only for messages
    originating from group chats.

    Returns:
        bool: True if the message was sent from a group, otherwise False.

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot.models import Update
        >>> from rubpy.bot.filters import group
        >>>
        >>> bot_client = BotClient("your_bot_token")
        >>>
        >>> @bot_client.on_update(group)
        ... async def handle_group_messages(c, update):
        ...     await c.send_message(update.chat_id, "This message came from a group!")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        return bool(update.chat_id.startswith("c0"))


class bot(Filter):
    """
    Filter for detecting messages sent by bots.

    This filter checks whether the sender of the message is of type `'Bot'`.
    It supports both regular updates and inline messages.

    Returns:
        bool: True if the message was sent by a bot, otherwise False.

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot.models import Update
        >>> from rubpy.bot.filters import bot
        >>>
        >>> bot_client = BotClient("your_bot_token")
        >>>
        >>> @bot_client.on_update(bot)
        ... async def handle_bot_messages(c, update):
        ...     await c.send_message(update.chat_id, "A bot sent this message!")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        sender_type = (
            update.new_message.sender_type
            if isinstance(update, Update) and update.new_message
            else update.updated_message.sender_type if update.updated_message else ""
        )
        if not sender_type:
            return False
        return sender_type == "Bot"


class chat(Filter):
    """
    Filter for matching specific chat IDs.

    This filter allows you to restrict a handler to updates coming from one or more specified chat IDs.
    It supports both a single chat ID (as a string) and a list of chat IDs.

    Args:
        chat_id (Union[list, str]): A single chat ID or a list of chat IDs to allow.

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot.models import Update
        >>> from rubpy.bot.filters import chat
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> @bot.on_update(chat("b0_test_chat"))
        ... async def only_for_test_chat(c, update):
        ...     await c.send_message(update.chat_id, "Hello from test chat!")
        >>>
        >>> @bot.on_update(chat(["b0_admin", "b0_mod"]))
        ... async def for_admins_and_mods(c, update):
        ...     await c.send_message(update.chat_id, "Hello admins and moderators!")
    """

    def __init__(self, chat_id: Union[List[str], str]):
        self.chats = [chat_id] if isinstance(chat_id, str) else chat_id

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        return update.chat_id in self.chats


class button(Filter):
    """
    Filter for button click interactions. Supports both direct string comparison and regex matching.

    This filter is useful for handling button presses in a bot framework. It checks whether
    the button's identifier (such as `button_id` or `callback_data`) matches the expected value.

    Args:
        button_id (str): The value to compare directly or match using a regex pattern.
        regex (bool): If True, treats the button_id as a regular expression.

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot.models import Update
        >>> from rubpy.bot.filters import button
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> @bot.on_update(button("btn_123"))
        ... async def handle_btn(c, update):
        ...     await c.send_message(update.chat_id, "Button 123 clicked!")
        >>>
        >>> @bot.on_update(button(r"btn_\\d+", regex=True))
        ... async def handle_regex_btn(c, update):
        ...     await c.send_message(update.chat_id, "Numbered button clicked!")
    """

    def __init__(self, button_id: str, regex: bool = False):
        self.regex = regex
        self.button_id = re.compile(button_id) if regex else button_id

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        aux_data = None

        # Extract aux_data depending on update type
        if isinstance(update, Update):
            message = update.new_message or update.updated_message
            if message:
                aux_data = message.aux_data
        elif isinstance(update, InlineMessage):
            aux_data = update.aux_data

        if not aux_data:
            return False

        # Retrieve button_id from aux_data, even if nested
        button_id = aux_data.get("button_id") or aux_data.get("callback_data")
        if not button_id:
            for value in aux_data.values():
                if isinstance(value, dict):
                    button_id = value.get("button_id") or value.get("callback_data")
                    if button_id:
                        break

        if not button_id:
            return False

        # Perform match
        if self.regex:
            return bool(self.button_id.match(button_id))
        else:
            return button_id == self.button_id


class forward(Filter):
    """
    Filter for checking forwarded messages.

    Returns:
        bool: True if the message forward matches the given criteria.

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot.filters import forward
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> # Match any forward message
        >>> @bot.on_update(forward)
        ... async def any_forward(c, update):
        ...     await update.reply("You sent some forward!")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        try:
            if bool(update.find_key("forwarded_no_link")):
                return True
            return bool(update.find_key("forwarded_from"))

        except KeyError:
            return False


class is_edited(Filter):
    """
    Filter for checking edited messages.

    Returns:
        bool: False or True

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot import filters
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> # Match any is_edited message
        >>> @bot.on_update(filters.is_edited)
        ... async def any_edited(c, update):
        ...     await update.delete()
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        try:
            return bool(update.find_key("is_edited"))

        except KeyError:
            return False


class sender_type(Filter):
    """
    Filter for matching specific sender types.

    This filter is used to allow or restrict handlers based on the `sender_type` field in an update.
    It supports both a single sender type as a string, or a list of allowed sender types.

    Args:
        types (Union[List[str], str]): A single sender type or a list of allowed sender types.
            Examples of sender types may include "user", "bot", "channel", etc.

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot.models import Update
        >>> from rubpy.bot.filters import sender_type
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> @bot.on_update(sender_type("User"))
        ... async def handle_user_message(c, update):
        ...     await c.send_message(update.chat_id, "Hello user!")
        >>>
        >>> @bot.on_update(sender_type(["Bot", "Channel"]))
        ... async def handle_bots_or_channels(c, update):
        ...     await c.send_message(update.chat_id, "Hello bot or channel!")
    """

    def __init__(self, types: Union[List[str], str]):
        self.types = [types] if isinstance(types, str) else types

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        try:
            sender_type = update.find_key("sender_type")
            return bool(sender_type in self.types)
        except KeyError:
            return False


class has_aux_data(Filter):
    """
    Filter for checking aux_data messages.

    Returns:
        bool: False or True

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot import filters
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> # Match any aux_data message
        >>> @bot.on_update(filters.has_aux_data)
        ... async def any_has_aux_data(c, update):
        ...     await update.reply("has aux data")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        try:
            return bool(update.find_key("aux_data"))

        except KeyError:
            return False


class file(Filter):
    """
    Filter for checking file messages.

    Returns:
        bool: False or True

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot import filters
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> # Match any file message
        >>> @bot.on_update(filters.file)
        ... async def any_file(c, update):
        ...     await update.reply("new file")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        try:
            return bool(update.find_key("file"))

        except KeyError:
            return False

class photo(Filter):
    """
    Filter for checking photo messages.

    Returns:
        bool: False or True

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot import filters
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> # Match any photo message
        >>> @bot.on_update(filters.photo)
        ... async def any_photo(c, update):
        ...     await update.reply("new photo")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        try:
            result = update.find_key("file")
            if result:
                result = mimetypes.guess_type(result.file_name)[0]
                if result:
                    return result.startswith("image/")
            return result

        except KeyError:
            return False

class video(Filter):
    """
    Filter for checking video messages.

    Returns:
        bool: False or True

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot import filters
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> # Match any video message
        >>> @bot.on_update(filters.video)
        ... async def any_video(c, update):
        ...     await update.reply("new video")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        try:
            result = update.find_key("file")
            if result:
                result = mimetypes.guess_type(result.file_name)[0]
                if result:
                    return result.startswith("video/")
            return result

        except KeyError:
            return False

class audio(Filter):
    """
    Filter for checking audio messages.

    Returns:
        bool: False or True

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot import filters
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> # Match any audio message
        >>> @bot.on_update(filters.audio)
        ... async def any_audio(c, update):
        ...     await update.reply("new audio")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        try:
            result = update.find_key("file")
            if result:
                result = mimetypes.guess_type(result.file_name)[0]
                if result:
                    return result.startswith("audio/") and not result.endswith("ogg")
            return result

        except KeyError:
            return False

class voice(Filter):
    """
    Filter for checking voice messages.

    Returns:
        bool: False or True

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot import filters
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> # Match any voice message
        >>> @bot.on_update(filters.voice)
        ... async def any_voice(c, update):
        ...     await update.reply("new voice")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        try:
            result = update.find_key("file")
            if result:
                result = mimetypes.guess_type(result.file_name)[0]
                if result:
                    return result == "audio/ogg"
            return result

        except KeyError:
            return False

class gif(Filter):
    """
    Filter for checking gif messages.

    Returns:
        bool: False or True

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot import filters
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> # Match any gif message
        >>> @bot.on_update(filters.gif)
        ... async def any_gif(c, update):
        ...     await update.reply("new gif")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        try:
            result = update.find_key("file")
            if result:
                result = mimetypes.guess_type(result.file_name)[0]
                if result:
                    return result.endswith("gif")
            return result

        except KeyError:
            return False

class location(Filter):
    """
    Filter for checking location messages.

    Returns:
        bool: False or True

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot import filters
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> # Match any location message
        >>> @bot.on_update(filters.location)
        ... async def any_location(c, update):
        ...     await update.reply("new location")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        try:
            return bool(update.find_key("location"))

        except KeyError:
            return False


class sticker(Filter):
    """
    Filter for checking sticker messages.

    Returns:
        bool: False or True

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot import filters
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> # Match any sticker message
        >>> @bot.on_update(filters.sticker)
        ... async def any_sticker(c, update):
        ...     await update.reply("new sticker")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        try:
            return bool(update.find_key("sticker"))

        except KeyError:
            return False


class contact_message(Filter):
    """
    Filter for checking contact_message messages.

    Returns:
        bool: False or True

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot import filters
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> # Match any contact_message message
        >>> @bot.on_update(filters.contact_message)
        ... async def any_contact_message(c, update):
        ...     await update.reply("new contact_message")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        try:
            return bool(update.find_key("contact_message"))

        except KeyError:
            return False


class poll(Filter):
    """
    Filter for checking poll messages.

    Returns:
        bool: False or True

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot import filters
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> # Match any poll message
        >>> @bot.on_update(filters.poll)
        ... async def any_poll(c, update):
        ...     await update.reply("new poll")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        try:
            return bool(update.find_key("poll"))

        except KeyError:
            return False


class live_location(Filter):
    """
    Filter for checking live_location messages.

    Returns:
        bool: False or True

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot import filters
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> # Match any live_location message
        >>> @bot.on_update(filters.live_location)
        ... async def any_live_location(c, update):
        ...     await update.reply("new live_location")
    """

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        try:
            return bool(update.find_key("live_location"))

        except KeyError:
            return False


class replied(Filter):
    async def check(self, update):
        try:
            return bool(update.find_key("reply_to_message_id"))
        except KeyError:
            return False

class metadata(Filter):
    async def check(self, update):
        try:
            return bool(update.find_key("metadata"))
        except KeyError:
            return False

class states(Filter):
    """
    Self-contained states filter that stores states in-memory (no external libs).

    - Use as a filter instance: `s = states("awaiting_email"); @bot.on_update(s) ...`
    - Also exposes methods to set/get/clear state for a given update:
        await s.set_state_for(update, "awaiting_email", expire=300)
        await s.get_state_for(update)
        await s.clear_state_for(update)

    Args:
        targets: None|str|List[str] - states to match (None => match any existing state).
        match_mode: "exact"|"regex"|"contains"|"any" (default "exact")
        scope: "user"|"chat"|"both" - where to look up the state keys in internal store
        check_keys: list of keys to check inside update payload before checking internal store
        auto_clear: bool - if True and matched => automatically clear stored state
        set_on_match: Optional[str] - if provided, set this new state on match
        expire: Optional[int] - default TTL (seconds) when using set_on_match (or when set_state_for uses expire)
        invert: bool - invert the match result
    """

    # in-memory stores shared between instances (module-level)
    _STORE: Dict[str, str] = {}
    _TTL_TASKS: Dict[str, asyncio.Task] = {}

    def __init__(
        self,
        targets: Optional[Union[str, List[str]]] = None,
        match_mode: str = "exact",
        scope: str = "user",
        check_keys: Optional[List[str]] = None,
        auto_clear: bool = False,
        set_on_match: Optional[str] = None,
        expire: Optional[int] = None,
        invert: bool = False,
    ):
        # normalize targets
        self.targets = [targets] if isinstance(targets, str) else (targets or None)
        assert match_mode in ("exact", "regex", "contains", "any")
        assert scope in ("user", "chat", "both")
        self.match_mode = match_mode
        self.scope = scope
        self.check_keys = check_keys or [
            "state",
            "fsm_state",
            "user_state",
            "session_state",
        ]
        self.auto_clear = auto_clear
        self.set_on_match = set_on_match
        self.default_expire = expire
        self.invert = invert

        if self.match_mode == "regex" and self.targets:
            self._patterns = [re.compile(p) for p in self.targets]
        else:
            self._patterns = None

    # -------------------------
    # Helper store / TTL logic
    # -------------------------
    @classmethod
    async def _schedule_expiry(cls, key: str, seconds: int):
        # cancel existing
        old = cls._TTL_TASKS.get(key)
        if old and not old.done():
            old.cancel()

        async def _job():
            try:
                await asyncio.sleep(seconds)
                cls._STORE.pop(key, None)
                cls._TTL_TASKS.pop(key, None)
            except asyncio.CancelledError:
                return

        t = asyncio.create_task(_job())
        cls._TTL_TASKS[key] = t

    @classmethod
    async def _set_store(cls, key: str, value: str, expire: Optional[int] = None):
        cls._STORE[key] = value
        if expire:
            await cls._schedule_expiry(key, expire)

    @classmethod
    async def _get_store(cls, key: str) -> Optional[str]:
        return cls._STORE.get(key)

    @classmethod
    async def _clear_store(cls, key: str):
        cls._STORE.pop(key, None)
        task = cls._TTL_TASKS.pop(key, None)
        if task and not task.done():
            task.cancel()

    # -------------------------
    # Public helper APIs
    # -------------------------
    async def set_state_for(
        self,
        update: Union[Update, InlineMessage, Any],
        value: str,
        expire: Optional[int] = None,
    ):
        """
        Set a state for the update's scope (user/chat) according to filter.scope.
        """
        klist = self._keys_for_update(update)
        if not klist:
            raise RuntimeError("Cannot determine key from update to set state")
        for k in klist:
            await self._set_store(k, value, expire or self.default_expire)

    async def get_state_for(
        self, update: Union[Update, InlineMessage, Any]
    ) -> Optional[str]:
        """Get first available state from storage for the update (according to scope)."""
        klist = self._keys_for_update(update)
        if not klist:
            return None
        for k in klist:
            v = await self._get_store(k)
            if v is not None:
                return v
        return None

    async def clear_state_for(self, update: Union[Update, InlineMessage, Any]):
        """Clear states (all keys derived from update)."""
        klist = self._keys_for_update(update)
        if not klist:
            return
        for k in klist:
            await self._clear_store(k)

    # -------------------------
    # internal helpers
    # -------------------------
    def _keys_for_update(self, update: Union[Update, InlineMessage, Any]) -> List[str]:
        """
        Build one or two keys to try based on scope and available ids on update.
        Keys look like "user:{sender_id}" and/or "chat:{chat_id}".
        """
        keys = []
        # try attributes first
        sender_id = getattr(update, "sender_id", None)
        chat_id = getattr(update, "chat_id", None)
        # fallback to find_key if exists
        try:
            if not sender_id and hasattr(update, "find_key"):
                sender_id = (
                    update.find_key("sender_id")
                    or update.find_key("from_id")
                    or sender_id
                )
        except Exception:
            pass
        try:
            if not chat_id and hasattr(update, "find_key"):
                chat_id = update.find_key("chat_id") or chat_id
        except Exception:
            pass

        if self.scope in ("user", "both") and sender_id:
            keys.append(f"user:{sender_id}")
        if self.scope in ("chat", "both") and chat_id:
            keys.append(f"chat:{chat_id}")
        return keys

    async def _extract_local_state(
        self, update: Union[Update, InlineMessage, Any]
    ) -> Optional[str]:
        """
        Try to read state directly from update payload keys (without using internal store).
        Returns first found string value or None.
        """
        for k in self.check_keys:
            try:
                if hasattr(update, "find_key"):
                    val = update.find_key(k)
                else:
                    val = getattr(update, k, None)
            except Exception:
                val = None
            if val:
                # if it's collection, pick first str
                if isinstance(val, (list, tuple, set)):
                    val = next((x for x in val if isinstance(x, str)), None)
                if isinstance(val, (str, int, float)):
                    return str(val)
        # also look inside aux_data if present
        try:
            aux = (
                update.find_key("aux_data")
                if hasattr(update, "find_key")
                else getattr(update, "aux_data", None)
            )
            if aux and isinstance(aux, dict):
                for k in ("state", "fsm_state"):
                    v = aux.get(k)
                    if v:
                        return str(v)
        except Exception:
            pass
        return None

    def _matches(self, value: str) -> bool:
        if self.match_mode == "any":
            return True if value else False
        if self.match_mode == "contains":
            return any(t in value for t in (self.targets or []))
        if self.match_mode == "regex" and self._patterns:
            return any(p.match(value) for p in self._patterns)
        # exact
        return value in (self.targets or [])

    # -------------------------
    # Filter entry point
    # -------------------------
    async def check(self, update: Union[Update, InlineMessage, Any]) -> bool:
        # 1. local payload
        local = await self._extract_local_state(update)
        state_val = None
        if local:
            state_val = local

        # 2. fallback to internal store
        if state_val is None:
            state_val = await self.get_state_for(update)

        matched = False if state_val is None else self._matches(state_val)

        # apply invert
        matched = (not matched) if self.invert else matched

        # side-effects
        if matched:
            # auto clear or set_on_match
            if self.auto_clear:
                await self.clear_state_for(update)
            if self.set_on_match:
                await self.set_state_for(
                    update, self.set_on_match, expire=self.default_expire
                )

        return matched
