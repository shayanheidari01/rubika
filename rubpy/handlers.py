import difflib
import inspect
#import warnings
import asyncio
import sys
from typing import Type
from .types import Update

AUTHORIZED_HANDLERS = [
    'ChatUpdates',
    'MessageUpdates',
    'ShowActivities',
    'ShowNotifications',
    'RemoveNotifications'
]

def create_handler(name, base, authorized_handlers: list = [], exception: bool = True, *args, **kwargs):
    result = name if name in authorized_handlers else difflib.get_close_matches(name, authorized_handlers, n=1)[0] if authorized_handlers else None

    if result is not None or not exception:
        return type(result, base, {'__name__': result, **kwargs}) if result is not None else None

    caller = inspect.getframeinfo(inspect.stack()[2][0])
    raise AttributeError(f'{caller.filename}:{caller.lineno}: Module has no attribute ({name})')

class BaseHandlers(Update):
    __name__ = 'CustomHandlers'

    def __init__(self, *models, any_handler: bool = False, **kwargs) -> None:
        self.__models = models
        self.__any_handler = any_handler

    def is_async(self, value, *args, **kwargs):
        return asyncio.iscoroutinefunction(value) or asyncio.iscoroutinefunction(value.__call__)

    async def __call__(self, update: dict, *args, **kwargs) -> bool:
        self.original_update = update

        if self.__models:
            for handler_filter in self.__models:
                if callable(handler_filter):
                    handler_filter = handler_filter(func=None) if isinstance(handler_filter, type) else handler_filter
                    status = await handler_filter(self, result=None) if self.is_async(handler_filter) else handler_filter(self, result=None)

                    if status and self.__any_handler:
                        return True
                    elif not status:
                        return False

        return True

class Handlers:
    def __init__(self, name, *args, **kwargs) -> None:
        self.__name__ = name

    def __eq__(self, value: object) -> bool:
        return BaseHandlers in value.__bases__

    def __dir__(self):
        return sorted(AUTHORIZED_HANDLERS)

    def __call__(self, name, *args, **kwargs):
        return self.__getattr__(name)(*args, **kwargs)

    def __getattr__(self, name):
        return create_handler(name, (BaseHandlers,), AUTHORIZED_HANDLERS)

sys.modules[__name__] = Handlers(__name__)
ChatUpdates: Type[BaseHandlers]
#MessageUpdates: Type[BaseHandlers]
ShowActivities: Type[BaseHandlers]
ShowNotifications: Type[BaseHandlers]
RemoveNotifications: Type[BaseHandlers]

# class MessageUpdates:
#     async def __call__(self, *args: difflib.Any, **kwds: difflib.Any) -> difflib.Any:
#         pass