import sys
from .struct import Struct
from ..gadgets import Classino


class BaseResults(Struct):
    __type__ = 'CustomResult'

    def __init__(self, update, *args, **kwargs) -> None:
        self.original_update = update


class Results(Classino):
    def __init__(self, name, *args, **kwargs) -> None:
        self.__name__ = name

    def __eq__(self, value: object) -> bool:
        return BaseResults in value.__bases__

    def __call__(self, name, *args, **kwargs):
        return self.__getattr__(name)(*args, **kwargs)

    def __getattr__(self, name):
        return self.create(name, (BaseResults,), exception=False)


sys.modules[__name__] = Results(__name__)
