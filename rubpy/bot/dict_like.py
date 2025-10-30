from dataclasses import fields, is_dataclass
from typing import Union, get_args, get_origin


class DictLike:
    """
    A class that allows attribute access via dictionary-like key lookup.

    Provides dictionary-style access (`obj[key]`) to attributes.
    Also supports `get(key, default)` method.

    Methods:
        find_key(key): Recursively searches for a key in nested attributes
                       and returns its value if found, else raises KeyError.

    Example:
        >>> class Example(DictLike):
        ...     def __init__(self):
        ...         self.a = 10
        ...         self.b = DictLike()
        ...         self.b.c = 20
        ...         self.b.d = DictLike()
        ...         self.b.d.e = 30
        ...
        >>> ex = Example()
        >>> ex['a']
        10
        >>> ex.get('a')
        10
        >>> ex.find_key('e')
        30
        >>> ex.find_key('x')
        Traceback (most recent call last):
            ...
        KeyError: 'x'
    """

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def find_key(self, key):
        """
        Recursively searches for the given key in self and nested DictLike attributes.

        Args:
            key (str): The key to search for.

        Returns:
            Any: The value corresponding to the key if found.

        Raises:
            KeyError: If the key is not found in self or nested attributes.
        """
        # Check current level
        if hasattr(self, key):
            return getattr(self, key)

        # Recursively check nested DictLike attributes
        for attr_name in dir(self):
            # Skip special/private attributes
            if attr_name.startswith("_"):
                continue

            attr_value = getattr(self, attr_name, None)
            if isinstance(attr_value, DictLike):
                try:
                    return attr_value.find_key(key)
                except KeyError:
                    pass  # Continue searching

        # Not found
        raise KeyError(key)

    def __post_init__(self):
        """
        Automatically convert nested dictionaries to DictLike subclasses after initialization.
        This runs automatically in dataclasses that inherit from DictLike.
        """
        if not is_dataclass(self):
            return  # Only process dataclass-based subclasses

        for field in fields(self):
            value = getattr(self, field.name)
            if value is None:
                continue

            target_type = field.type

            # unwrap Optional[...], Union[..., None]
            if get_origin(target_type) is Union:
                args = get_args(target_type)
                target_type = next((arg for arg in args if arg is not type(None)), None)

            # DictLike single object
            if (
                isinstance(value, dict)
                and isinstance(target_type, type)
                and issubclass(target_type, DictLike)
            ):
                setattr(self, field.name, target_type(**value))

            # List[DictLike] support
            elif isinstance(value, list) and get_origin(target_type) is list:
                inner_type = get_args(target_type)[0]
                if isinstance(inner_type, type) and issubclass(inner_type, DictLike):
                    setattr(
                        self,
                        field.name,
                        [inner_type(**v) if isinstance(v, dict) else v for v in value],
                    )


__all__ = [
    "DictLike",
]
