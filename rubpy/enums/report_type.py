from enum import Enum

class ReportType(int, Enum):
    OTHER = 100
    VIOLENCE = 101
    SPAM = 102
    PORNOGRAPHY = 103
    CHILD_ABUSE = 104
    COPYRIGHT = 105
    FISHING = 106