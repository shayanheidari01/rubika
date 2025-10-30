import re
import time
import asyncio
from collections import defaultdict, deque
from typing import Optional

# Define regular expressions for patterns
RUBIKA_LINK_PATTERN = re.compile(r"\brubika\.ir\b")
GROUP_LINK_PATTERN = re.compile(r"https://rubika\.ir/joing/[A-Z0-9]+")
CHANNEL_LINK_PATTERN = re.compile(r"https://rubika\.ir/joing/[A-Z0-9]+")
USERNAME_PATTERN = re.compile(r"@([a-zA-Z0-9_]{4,32})")


# Functions to check patterns
def is_rubika_link(string: str) -> bool:
    """
    Check if the given string contains a Rubika link.

    :param string: Input string to check.
    :return: True if the string contains a Rubika link, False otherwise.
    """
    return bool(RUBIKA_LINK_PATTERN.search(string))


def is_group_link(string: str) -> bool:
    """
    Check if the given string contains a Rubika group link.

    :param string: Input string to check.
    :return: True if the string contains a Rubika group link, False otherwise.
    """
    return bool(GROUP_LINK_PATTERN.search(string))


def is_channel_link(string: str) -> bool:
    """
    Check if the given string contains a Rubika channel link.

    :param string: Input string to check.
    :return: True if the string contains a Rubika channel link, False otherwise.
    """
    return bool(CHANNEL_LINK_PATTERN.search(string))


def is_username(string: str) -> bool:
    """
    Check if the given string contains a Rubika username.

    :param string: Input string to check.
    :return: True if the string contains a Rubika username, False otherwise.
    """
    return bool(USERNAME_PATTERN.search(string))


# Functions to extract matches
def get_rubika_links(string: str) -> list:
    """
    Extract Rubika links from the given string.

    :param string: Input string to extract links from.
    :return: List of Rubika links found in the string.
    """
    return RUBIKA_LINK_PATTERN.findall(string)


def get_group_links(string: str) -> list:
    """
    Extract Rubika group links from the given string.

    :param string: Input string to extract group links from.
    :return: List of Rubika group links found in the string.
    """
    return GROUP_LINK_PATTERN.findall(string)


def get_channel_links(string: str) -> list:
    """
    Extract Rubika channel links from the given string.

    :param string: Input string to extract channel links from.
    :return: List of Rubika channel links found in the string.
    """
    return CHANNEL_LINK_PATTERN.findall(string)


def get_usernames(string: str) -> list:
    """
    Extract Rubika usernames from the given string.

    :param string: Input string to extract usernames from.
    :return: List of Rubika usernames found in the string.
    """
    return USERNAME_PATTERN.findall(string)


# Text formatting functions
def Bold(text: str) -> str:
    """
    Make the text bold.

    :param text: Input text to be formatted.
    :return: Bold formatted text.
    """
    return f"**{text.strip()}**"


def Italic(text: str) -> str:
    """
    Make the text italic.

    :param text: Input text to be formatted.
    :return: Italic formatted text.
    """
    return f"_{text.strip()}"


def Underline(text: str) -> str:
    """
    Underline the text.

    :param text: Input text to be formatted.
    :return: Underlined text.
    """
    return f"--{text.strip()}--"


def Strike(text: str) -> str:
    """
    Add strike-through to the text.

    :param text: Input text to be formatted.
    :return: Text with strike-through.
    """
    return f"~~{text.strip()}~~"


def Spoiler(text: str) -> str:
    """
    Format the text as a spoiler.

    :param text: Input text to be formatted.
    :return: Spoiler formatted text.
    """
    return f"||{text.strip()}||"


def Code(text: str) -> str:
    """
    Format the text as code.

    :param text: Input text to be formatted.
    :return: Code formatted text.
    """
    return f"`{text.strip()}`"


def Mention(text: str, object_guid: str) -> str:
    """
    Mention a user with a specific object GUID.

    :param text: Text to be mentioned.
    :param object_guid: GUID of the mentioned object.
    :return: Mention formatted text.
    """
    return f"[{text.strip()}]({object_guid.strip()})"


def Hyperlink(text: str, link: str) -> str:
    """
    Create a hyperlink with the provided text and link.

    :param text: Text for the hyperlink.
    :param link: URL for the hyperlink.
    :return: Hyperlink formatted text.
    """
    return f"[{text.strip()}]({link.strip()})"


class AntiSpam:
    """
    Advanced Anti-Spam System for Bots (Groups & Private)

    Features:
    - Per chat_id spam protection (group & private)
    - Max messages per time window
    - Auto block duration
    - Auto clear expired blocks
    - Max message length check

    Example:
    --------
    antispam = AntiSpam()

    # Check spam in group
    if await antispam.is_spammer(chat_id=123, user_id=456, message="hello"):
        print("User is spamming in group!")

    # Check spam in private chat
    if await antispam.is_spammer(chat_id=456, message="hi"):
        print("User is spamming in private!")
    """

    def __init__(
        self,
        max_msg_per_window: int = 5,
        time_window: int = 10,
        block_duration: int = 30,
        max_message_length: int = 1000,
        auto_clear_interval: int = 5,
        auto_clear_expire: int = 20,
    ):
        # Spam settings
        self.max_msg_per_window = max_msg_per_window
        self.time_window = time_window
        self.block_duration = block_duration
        self.max_message_length = max_message_length
        self.auto_clear_expire = auto_clear_expire

        # Storage
        self.user_message_times = defaultdict(lambda: deque(maxlen=max_msg_per_window))
        self.blocked_users = {}  # (chat_id, user_id) -> block_time
        self.notified_users = set()

        # Auto clear loop
        self._auto_clear_task = asyncio.create_task(self._auto_clear(auto_clear_interval))

    def _make_key(self, chat_id: str, user_id: Optional[str], is_private: bool) -> tuple:
        """Generate unique key for spam tracking"""
        if is_private:
            return (f"private_{chat_id}", None)
        return (chat_id, user_id)

    async def is_spammer(
        self, chat_id: str, user_id: Optional[str] = None, message: str = ""
    ) -> bool:
        """Check if user is spammer"""
        now = time.time()
        key = self._make_key(chat_id, user_id, True if user_id else False)

        # Message length check
        if message and len(message) > self.max_message_length:
            self.blocked_users[key] = now
            return True

        # Already blocked
        if key in self.blocked_users:
            if now - self.blocked_users[key] < self.block_duration:
                return True
            else:
                del self.blocked_users[key]
                self.notified_users.discard(key)

        # Add message timestamp
        self.user_message_times[key].append(now)

        # Spam detection
        if len(self.user_message_times[key]) == self.max_msg_per_window:
            if now - self.user_message_times[key][0] < self.time_window:
                self.blocked_users[key] = now
                return True

        return False

    async def _auto_clear(self, interval: int):
        """Auto clear expired blocks to free memory"""
        while True:
            await asyncio.sleep(interval)
            now = time.time()

            # Clear expired blocks
            expired = [
                key for key, t in self.blocked_users.items() if now - t > self.auto_clear_expire
            ]
            for key in expired:
                del self.blocked_users[key]
                self.notified_users.discard(key)

            # Also clear old message times
            for key in list(self.user_message_times.keys()):
                if not self.user_message_times[key]:
                    del self.user_message_times[key]