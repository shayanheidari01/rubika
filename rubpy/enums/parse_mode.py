from enum import Enum


class ParseMode(str, Enum):
    HTML = 'html'
    MARKDOWN = 'markdown'