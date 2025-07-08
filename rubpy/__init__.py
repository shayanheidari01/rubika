from .sessions import SQLiteSession, StringSession
from .client import Client
from .rubino import Rubino
from . import types, utils, filters, exceptions, enums, sync

__author__ = 'Shayan Heidari'
__version__ = '6.8.5'
__license__ = 'GNU Lesser General Public License v3 (LGPLv3)'
__welcome__ = (
    f'Welcome to Rubpy (version {__version__})\n'
    'Rubpy is free software and comes with ABSOLUTELY NO WARRANTY. Licensed\n'
    f'under the terms of the {__license__}.\n\n'
)