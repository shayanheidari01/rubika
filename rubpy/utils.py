import re

# Define regular expressions for patterns
RUBIKA_LINK_PATTERN = re.compile(r'\brubika\.ir\b')
GROUP_LINK_PATTERN = re.compile(r'https://rubika\.ir/joing/[A-Z0-9]+')
CHANNEL_LINK_PATTERN = re.compile(r'https://rubika\.ir/joing/[A-Z0-9]+')
USERNAME_PATTERN = re.compile(r'@([a-zA-Z0-9_]{3,32})')

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
    return f'**{text.strip()}**'

def Italic(text: str) -> str:
    """
    Make the text italic.

    :param text: Input text to be formatted.
    :return: Italic formatted text.
    """
    return f'_{text.strip()}'

def Underline(text: str) -> str:
    """
    Underline the text.

    :param text: Input text to be formatted.
    :return: Underlined text.
    """
    return f'--{text.strip()}--'

def Strike(text: str) -> str:
    """
    Add strike-through to the text.

    :param text: Input text to be formatted.
    :return: Text with strike-through.
    """
    return f'~~{text.strip()}~~'

def Spoiler(text: str) -> str:
    """
    Format the text as a spoiler.

    :param text: Input text to be formatted.
    :return: Spoiler formatted text.
    """
    return f'||{text.strip()}||'

def Code(text: str) -> str:
    """
    Format the text as code.

    :param text: Input text to be formatted.
    :return: Code formatted text.
    """
    return f'`{text.strip()}`'

def Mention(text: str, object_guid: str) -> str:
    """
    Mention a user with a specific object GUID.

    :param text: Text to be mentioned.
    :param object_guid: GUID of the mentioned object.
    :return: Mention formatted text.
    """
    return f'[{text.strip()}]({object_guid.strip()})'

def HyperLink(text: str, link: str) -> str:
    """
    Create a hyperlink with the provided text and link.

    :param text: Text for the hyperlink.
    :param link: URL for the hyperlink.
    :return: Hyperlink formatted text.
    """
    return f'[{text.strip()}]({link.strip()})'
