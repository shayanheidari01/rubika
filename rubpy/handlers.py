import sys
import difflib
import inspect
import warnings
import asyncio
from .types import SocketResults


__handlers__ = [
    'ChatUpdates',
    'MessageUpdates',
    'ShowActivities',
    'ShowNotifications',
    'RemoveNotifications'
]

def create(name, __base, authorise: list = [], exception: bool = True, *args, **kwargs):
        result = None
        if name in authorise:
            result = name

        else:
            proposal = difflib.get_close_matches(name, authorise, n=1)
            if proposal:
                result = proposal[0]
                caller = inspect.getframeinfo(inspect.stack()[2][0])
                warnings.warn(
                    f'{caller.filename}:{caller.lineno}: do you mean'
                    f' "{name}", "{result}"? correct it')

        if result is not None or not exception:
            if result is None:
                result = name
            return type(result, __base, {'__name__': result, **kwargs})

        raise AttributeError(f'module has no attribute ({name})')


class BaseHandlers(SocketResults):
    __name__ = 'CustomHandlers'

    def __init__(self, *models, __any: bool = False, **kwargs) -> None:
        self.__models = models
        self.__any = __any

    def is_async(self, value, *args, **kwargs):
        result = False
        if asyncio.iscoroutinefunction(value):
            result = True

        elif asyncio.iscoroutinefunction(value.__call__):
            result = True

        return result

    async def __call__(self, update: dict, *args, **kwargs) -> bool:
        self.original_update = update
        if self.__models:
            for filter in self.__models:
                if callable(filter):
                    # if BaseModels is not called
                    if isinstance(filter, type):
                        filter = filter(func=None)

                    if self.is_async(filter):
                        status = await filter(self, result=None)

                    else:
                        status = filter(self, result=None)

                    if status and self.__any:
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
        return sorted(__handlers__)

    def __call__(self, name, *args, **kwargs):
        return self.__getattr__(name)(*args, **kwargs)

    def __getattr__(self, name):
        return create(name, (BaseHandlers,), __handlers__)

sys.modules[__name__] = Handlers(__name__)
