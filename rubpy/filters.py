from typing import Callable, Union, List, Pattern, Type
import difflib
import inspect
import warnings
import sys
import re

__all__ = ['Operator', 'BaseModel', 'RegexModel',
           'AuthorGuids', 'ObjectGuids', 'Commands']
__models__ = [
    'is_pinned', 'is_mute', 'count_unseen', 'message_id',
    'is_group', 'is_private', 'is_channel', 'is_in_contact',
    'raw_text', 'original_update', 'object_guid', 'author_guid',
    'time', 'reply_message_id']

def create_model(name, base, authorize: list = [], exception: bool = True, *args, **kwargs):
    result = None
    if name in authorize:
        result = name
    else:
        proposal = difflib.get_close_matches(name, authorize, n=1)
        if proposal:
            result = proposal[0]
            caller = inspect.getframeinfo(inspect.stack()[2][0])
            warnings.warn(
                f'{caller.filename}:{caller.lineno}: Do you mean'
                f' "{name}", "{result}"? Correct it.')

    if result is not None or not exception:
        if result is None:
            result = name
        return type(result, base, {'__name__': result, **kwargs})

    raise AttributeError(f'Module has no attribute ({name})')


class Operator:
    Or = 'OR'
    And = 'AND'
    Less = 'Less'
    Lesse = 'Lesse'
    Equal = 'Equal'
    Greater = 'Greater'
    Greatere = 'Greatere'
    Inequality = 'Inequality'

    def __init__(self, value, operator, *args, **kwargs):
        self.value = value
        self.operator = operator

    def __eq__(self, value) -> bool:
        return self.operator == value


class BaseModel:
    def __init__(self, func=None, filters=[], *args, **kwargs) -> None:
        self.func = func
        if not isinstance(filters, list):
            filters = [filters]
        self.filters = filters

    def insert(self, filter):
        self.filters.append(filter)
        return self

    def __or__(self, value):
        return self.insert(Operator(value, Operator.Or))

    def __and__(self, value):
        return self.insert(Operator(value, Operator.And))

    def __eq__(self, value):
        return self.insert(Operator(value, Operator.Equal))

    def __ne__(self, value):
        return self.insert(Operator(value, Operator.Inequality))

    def __lt__(self, value):
        return self.insert(Operator(value, Operator.Less))

    def __le__(self, value):
        return self.insert(Operator(value, Operator.Lesse))

    def __gt__(self, value):
        return self.insert(Operator(value, Operator.Greater))

    def __ge__(self, value):
        return self.insert(Operator(value, Operator.Greatere))

    async def build(self, update):
        result = getattr(update, self.__class__.__name__, None)
        if callable(self.func):
            if update.is_async(self.func):
                result = await self.func(result)
            else:
                result = self.func(result)

        for filter in self.filters:
            value = filter.value

            if callable(value):
                if update.is_async(value):
                    value = await value(update, result)
                else:
                    value = value(update, result)

            if self.func:
                if update.is_async(self.func):
                    value = await self.func(value)
                else:
                    value = self.func(value)

            if filter == Operator.Or:
                result = result or value
            elif filter == Operator.And:
                result = result and value
            elif filter == Operator.Less:
                result = result < value
            elif filter == Operator.Lesse:
                result = result <= value
            elif filter == Operator.Equal:
                result = result == value
            elif filter == Operator.Greater:
                result = result > value
            elif filter == Operator.Greatere:
                result = result >= value
            elif filter == Operator.Inequality:
                result = result != value

        return bool(result)

    async def __call__(self, update, *args, **kwargs):
        return await self.build(update)


class Commands(BaseModel):
    def __init__(
            self,
            commands: Union[str, List[str]],
            prefixes: Union[str, List[str]] = "/",
            case_sensitive: bool = False, *args, **kwargs,
    ) -> None:
        """Filter Commands, i.e.: text messages starting with "/" or any other custom prefix.

        Parameters:
            commands (``str`` | ``list``):
                The command or list of commands as string the filter should look for.
                Examples: "start", ["start", "help", "settings"]. When a message text containing
                a command arrives, the command itself and its arguments will be stored in the *command*
                field of the :obj:`~pyrogram.types.Message`.

            prefixes (``str`` | ``list``, *optional*):
                A prefix or a list of prefixes as string the filter should look for.
                Defaults to "/" (slash). Examples: ".", "!", ["/", "!", "."], list(".:!").
                Pass None or "" (empty string) to allow commands with no prefix at all.

            case_sensitive (``bool``, *optional*):
                Pass True if you want your command(s) to be case sensitive. Defaults to False.
                Examples: when True, command="Start" would trigger /Start but not /start.
        """

        super().__init__(*args, **kwargs)
        self.command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")
        commands = commands if isinstance(commands, list) else [commands]
        commands = {c if case_sensitive else c.lower() for c in commands}

        prefixes = [] if prefixes is None else prefixes
        prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
        prefixes = set(prefixes) if prefixes else {""}

        self.commands = commands
        self.prefixes = prefixes
        self.case_sensitive = case_sensitive

    async def __call__(self, update, *args, **kwargs) -> bool:
        username = ""
        text = update.raw_text
        update['command'] = None

        if not text:
            return False

        for prefix in self.prefixes:
            if not text.startswith(prefix):
                continue

            without_prefix = text[len(prefix):]

            for cmd in self.commands:
                if not re.match(rf"^(?:{cmd}(?:@?{username})?)(?:\s|$)", without_prefix,
                                flags=re.IGNORECASE if not self.case_sensitive else 0):
                    continue

                without_command = re.sub(rf"{cmd}(?:@?{username})?\s?", "", without_prefix, count=1,
                                         flags=re.IGNORECASE if not self.case_sensitive else 0)

                # match.groups are 1-indexed, group(1) is the quote, group(2) is the text
                # between the quotes, group(3) is unquoted, whitespace-split text

                # Remove the escape character from the arguments
                update['command'] = [cmd] + [
                    re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                    for m in self.command_re.finditer(without_command)
                ]

                return True

        return False


class RegexModel(BaseModel):
    def __init__(self, pattern: str, *args, **kwargs) -> None:
        self.pattern = re.compile(pattern)
        super().__init__(*args, **kwargs)

    async def __call__(self, update, *args, **kwargs) -> bool:
        if update.raw_text is None:
            return False

        update.pattern_match = self.pattern.match(update.raw_text)
        return bool(update.pattern_match)


class ObjectGuids(BaseModel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.object_guids = []
        for arg in args:
            if isinstance(arg, list):
                self.object_guids.extend(arg)
            elif isinstance(arg, tuple):
                self.object_guids.extend(list(arg))
            else:
                self.object_guids.append(arg)

    async def __call__(self, update, *args, **kwargs) -> bool:
        if update.object_guid is None:
            return False

        return update.object_guid in self.object_guids


class AuthorGuids(BaseModel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.author_guids = []
        for arg in args:
            if isinstance(arg, list):
                self.author_guids.extend(arg)
            elif isinstance(arg, tuple):
                self.author_guids.extend(list(arg))
            else:
                self.author_guids.append(arg)

    async def __call__(self, update, *args, **kwargs) -> bool:
        if update.author_guid is None:
            return False

        return update.author_guid in self.author_guids


class Models:
    def __init__(self, name, *args, **kwargs) -> None:
        self.__name__ = name

    def __eq__(self, value: object) -> bool:
        return BaseModel in value.__bases__

    def __dir__(self):
        return sorted(__models__)

    def __call__(self, name, *args, **kwargs):
        return self.__getattr__(name)

    def __getattr__(self, name):
        if name in __all__:
            return globals()[name]
        return create_model(name, (BaseModel,), authorize=__models__, exception=False)

sys.modules[__name__] = Models(__name__)

is_pinned: Type[BaseModel]
is_mute: Type[BaseModel]
count_unseen: Type[BaseModel]
message_id: Type[BaseModel]
is_group: Type[BaseModel]
is_private: Type[BaseModel]
is_channel: Type[BaseModel]
is_in_contact: Type[BaseModel]
raw_text: Type[BaseModel]
original_update: Type[BaseModel]
object_guid: Type[BaseModel]
author_guid: Type[BaseModel]
time: Type[BaseModel]
reply_message_id: Type[BaseModel]