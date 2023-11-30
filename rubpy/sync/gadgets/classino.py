import difflib
import inspect
import warnings

class Classino:

    @classmethod
    def create(cls, name, __base, authorise: list = [], exception: bool = True, *args, **kwargs):
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

        print(f'module has no attribute ({name})')