import re

RUBIKA_LINK_PATTERN = re.compile(r'\brubika\.ir\b')
GROUP_LINK_PATTERN = re.compile(r'https://rubika\.ir/joing/[A-Z0-9]+')
USERNAME_PATTERN = re.compile(r'@([a-zA-Z0-9_]{3,20})')

def is_rubika_link(string: str) -> bool:
    return bool(RUBIKA_LINK_PATTERN.search(string))

def is_group_link(string: str) -> bool:
    return bool(GROUP_LINK_PATTERN.search(string))

def is_username(string: str) -> bool:
    return bool(USERNAME_PATTERN.search(string))

def get_rubika_links(string: str) -> list:
    return RUBIKA_LINK_PATTERN.findall(string)

def get_group_links(string: str) -> list:
    return GROUP_LINK_PATTERN.findall(string)

def get_usernames(string: str) -> list:
    return USERNAME_PATTERN.findall(string)

def Bold(text: str) -> str:
    return f'**{text.strip()}**'

def Italic(text: str) -> str:
    return f'__{text.strip()}__'

def Underline(text: str) -> str:
    return f'--{text.strip()}--'

def Strike(text: str) -> str:
    return f'~~{text.strip()}~~'

def Spoiler(text: str) -> str:
    return f'||{text.strip()}||'

def Code(text: str):
    return f'`{text.strip()}`'

def Mention(text: str, object_guid: str) -> str:
    return f'[{text.strip()}]({object_guid.strip()})'

def HyperLink(text: str, link: str) -> str:
    return f'[{text.strip()}]({link.strip()})'