from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, MutableMapping, Optional, Tuple, TYPE_CHECKING, Awaitable, Union

if TYPE_CHECKING:  # pragma: no cover - imported for type checking only
    from rubpy.bot.bot import BotClient


@dataclass(frozen=True)
class PluginMeta:
    """Metadata describing a plugin package."""

    name: str
    version: str = "0.0.0"
    description: str = ""
    author: str = ""
    homepage: Optional[str] = None
    dependencies: Tuple[str, ...] = ()
    default_config: Mapping[str, Any] = field(default_factory=dict)


class Plugin:
    """Base class that every Rubpy plugin must inherit from."""

    meta = PluginMeta(name="unnamed")

    def __init__(self, bot: "BotClient", *, config: Optional[Mapping[str, Any]] = None) -> None:
        self.bot = bot
        self.config = self._merge_config(config)

    def setup(self) -> Optional[Union[Awaitable[None], None]]:  # pragma: no cover - overridable hook
        """Hook executed when the plugin is enabled. Can be sync or async."""
        return None

    def teardown(self) -> Optional[Union[Awaitable[None], None]]:  # pragma: no cover - overridable hook
        """Hook executed when the plugin is disabled. Can be sync or async."""
        return None

    def configure(self, config: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
        """Override to validate/extend merged configuration before it is stored."""
        return config

    def get_config(self, key: str, default: Optional[Any] = None) -> Any:
        """Convenience access to the resolved configuration mapping."""
        return self.config.get(key, default)

    def _merge_config(self, override: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
        defaults = getattr(self.meta, "default_config", None) or {}
        merged: Dict[str, Any] = dict(defaults)
        if override:
            merged.update(override)

        configured = self.configure(merged)
        if configured is None:
            return merged
        if not isinstance(configured, Mapping):
            raise TypeError("Plugin.configure() must return a mapping or None")
        return dict(configured)

    @classmethod
    def identifier(cls) -> str:
        """Return the registry identifier for this plugin."""
        if cls.meta and cls.meta.name and cls.meta.name != "unnamed":
            return cls.meta.name
        return cls.__name__
