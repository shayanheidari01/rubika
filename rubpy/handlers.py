import difflib
import inspect
import asyncio
import sys
from typing import Type
from .types import Update

# List of authorized handlers
AUTHORIZED_HANDLERS = [
    'ChatUpdates',
    'MessageUpdates',
    'ShowActivities',
    'ShowNotifications',
    'RemoveNotifications'
]

def create_handler(name, base, authorized_handlers: list = [], exception: bool = True, *args, **kwargs):
    """
    Create a handler dynamically based on the given name and base class.

    :param name: Name of the handler.
    :param base: Base class for the handler.
    :param authorized_handlers: List of authorized handler names.
    :param exception: Whether to raise an exception if the handler is not authorized.
    :param args: Additional positional arguments.
    :param kwargs: Additional keyword arguments.
    :return: Dynamically created handler class.
    """
    result = name if name in authorized_handlers else difflib.get_close_matches(name, authorized_handlers, n=1)[0] if authorized_handlers else None

    if result is not None or not exception:
        return type(result, base, {'__name__': result, **kwargs}) if result is not None else None

    caller = inspect.getframeinfo(inspect.stack()[2][0])
    raise AttributeError(f'{caller.filename}:{caller.lineno}: Module has no attribute ({name})')

class BaseHandlers(Update):
    """
    Base class for custom handlers.

    :param models: List of models.
    :param any_handler: Whether any handler should be executed.
    :param kwargs: Additional keyword arguments.
    """
    __name__ = 'CustomHandlers'

    def __init__(self, *models, any_handler: bool = False, **kwargs) -> None:
        self.__models = models
        self.__any_handler = any_handler

    def is_async(self, value, *args, **kwargs):
        """
        Check if the given function is asynchronous.

        :param value: Function to check.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: True if the function is asynchronous, False otherwise.
        """
        return asyncio.iscoroutinefunction(value) or asyncio.iscoroutinefunction(value.__call__)

    async def __call__(self, update: dict, *args, **kwargs) -> bool:
        """
        Execute the handler on the given update.

        :param update: Update dictionary.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: True if the handler should be executed, False otherwise.
        """
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
    """
    Class to handle and create specific handlers.
    """

    def __init__(self, name, *args, **kwargs) -> None:
        self.__name__ = name

    def __eq__(self, value: object) -> bool:
        """
        Check if the given value is equal to the base handlers class.

        :param value: Value to check.
        :return: True if equal, False otherwise.
        """
        return BaseHandlers in value.__bases__

    def __dir__(self):
        """
        Get the list of authorized handlers.

        :return: Sorted list of authorized handlers.
        """
        return sorted(AUTHORIZED_HANDLERS)

    def __call__(self, name, *args, **kwargs):
        """
        Call the handler based on the given name.

        :param name: Name of the handler.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: Dynamically created handler class.
        """
        return self.__getattr__(name)(*args, **kwargs)

    def __getattr__(self, name):
        """
        Get the dynamically created handler based on the name.

        :param name: Name of the handler.
        :return: Dynamically created handler class.
        """
        return create_handler(name, (BaseHandlers,), AUTHORIZED_HANDLERS)

# Replace the current module with an instance of Handlers
sys.modules[__name__] = Handlers(__name__)

# Define specific handler types
ChatUpdates: Type[BaseHandlers]
MessageUpdates: Type[BaseHandlers]
ShowActivities: Type[BaseHandlers]
ShowNotifications: Type[BaseHandlers]
RemoveNotifications: Type[BaseHandlers]
