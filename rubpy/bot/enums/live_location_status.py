from enum import Enum


class LiveLocationStatus(str, Enum):
    Stopped = 'Stopped'
    Live = 'Live'