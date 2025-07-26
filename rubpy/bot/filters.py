# Filters
import re
from typing import List, Optional, Union
import warnings

from rubpy.bot.enums.forwarded_from_type import ForwardedFromType
from rubpy.bot.models import Update
from rubpy.bot.models import InlineMessage


class Filter:
    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        return True

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

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        text = update.find_key('text')
        if not text:
            return False
        if not self.text and not self.regex:
            return True
        return bool(re.match(self.text, text)) if self.regex else text == self.text

class commands(Filter):
    """
    Filter for detecting command messages (e.g. /start, /help).

    This filter checks whether the message text starts with one of the specified slash commands.
    It is useful for handling bot commands in both private and group chats.

    Args:
        command (Union[str, List[str]]): A single command or list of command names (without the leading slash).

    Returns:
        bool: True if the message text starts with one of the specified commands.

    Example:
        >>> from rubpy import BotClient
        >>> from rubpy.bot.filters import commands
        >>>
        >>> bot = BotClient("your_bot_token")
        >>>
        >>> @bot.on_update(commands("start"))
        ... async def handle_start(c, update):
        ...     await c.send_message(update.chat_id, "Welcome to the bot!")
        >>>
        >>> @bot.on_update(commands(["help", "about"]))
        ... async def handle_help_about(c, update):
        ...     await c.send_message(update.chat_id, "Help or About command detected!")
    """

    def __init__(self, command: Union[str, List[str]]):
        self.commands = [command] if isinstance(command, str) else command

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        text = (
            update.new_message.text
            if isinstance(update, Update) and update.new_message
            else update.text
            if isinstance(update, InlineMessage)
            else ""
        )
        if not text:
            return False
        return any(text.startswith(f"/{cmd}") for cmd in self.commands)

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
        self.update_types = [update_types] if isinstance(update_types, str) else update_types

    async def check(self, update: Union[Update, InlineMessage]) -> bool:
        result = (
            (isinstance(update, Update) and update.type in self.update_types)
            or (isinstance(update, InlineMessage) and "InlineMessage" in self.update_types)
        )
        # logger.info(f"UpdateTypeFilter check for types={self.update_types}, update={type(update).__name__}: {result}")
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
        return update.new_message.sender_type == 'User'

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
        sender_type = (
            update.new_message.sender_type
            if isinstance(update, Update) and update.new_message
            else update.updated_message.sender_type
            if update.updated_message else ""
        )
        if not sender_type:
            return False
        return sender_type == 'Group'

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
            else update.updated_message.sender_type
            if update.updated_message else ""
        )
        if not sender_type:
            return False
        return sender_type == 'Bot'

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
            if bool(update.find_key('forwarded_no_link')):
                return True
            return bool(update.find_key('forwarded_from'))
        
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
            return bool(update.find_key('is_edited'))

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
            sender_type = update.find_key('sender_type')
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
            return bool(update.find_key('aux_data'))

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
            return bool(update.find_key('file'))

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
            return bool(update.find_key('location'))

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
            return bool(update.find_key('sticker'))

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
            return bool(update.find_key('contact_message'))

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
            return bool(update.find_key('poll'))

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
            return bool(update.find_key('live_location'))

        except KeyError:
            return False