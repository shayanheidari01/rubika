from .sessions import SQLiteSession, StringSession
from .client import Client
from .rubino import Rubino
from . import types, utils, filters, exceptions, enums, sync
from .bot import BotClient
from . import bot

__author__ = 'Rubpy Project'
__version__ = '7.2.0'
__license__ = 'GNU Lesser General Public License v3 (LGPLv3)'
__welcome__ = (
    f'Welcome to Rubpy (version {__version__})\n'
    'Rubpy is free software and comes with ABSOLUTELY NO WARRANTY. Licensed\n'
    f'under the terms of the {__license__}.\n\n'
)