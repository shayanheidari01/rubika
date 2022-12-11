from .accounts._client import _Client as Client
from .accounts.methods import Methods
from .bots.methods import Methods as BotMethods
from .bots import _Client as Bot
from .crypto import Crypto
from .util import Utils
from .exceptions import (
    InvaildAuth,
    InvalidInput,
    TooRequests,
    Repeated,
    NotRegistered,
    APIException,
)


__version__ = '5.2.0'
__author__ = 'Shayan Heidari'