from __future__ import annotations

import inspect
import logging
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Set, Type, TYPE_CHECKING

try:  # pragma: no cover - fallback for Python <3.8
    from importlib import metadata as importlib_metadata
except ImportError:  # pragma: no cover - fallback for Python 3.7
    import importlib_metadata  # type: ignore

from .base import Plugin

if TYPE_CHECKING:  # pragma: no cover - typing imports only
    from rubpy.bot.bot import BotClient

logger = logging.getLogger(__name__)


class PluginDefinitionError(RuntimeError):
    """Raised when a plugin definition is invalid."""


class PluginLoadError(RuntimeError):
    """Raised when a plugin fails to load or run hooks."""


class PluginManager:
    """Registers, discovers, and manages Rubpy plugins."""

    def __init__(
        self,
        bot: "BotClient",
        *,
        entry_point_group: str = "rubpy.plugins",
        auto_discover: bool = True,
        plugin_configs: Optional[Mapping[str, Mapping[str, object]]] = None,
    ) -> None:
        self.bot = bot
        self.entry_point_group = entry_point_group
        self._registry: Dict[str, Type[Plugin]] = {}
        self._display_names: Dict[str, str] = {}
        self._instances: Dict[str, Plugin] = {}
        self._enabled: Dict[str, Plugin] = {}
        self._configs: Dict[str, Mapping[str, object]] = {}
        self._enabling_stack: Set[str] = set()
        if plugin_configs:
            for identifier, config in plugin_configs.items():
                self._configs[self._normalize(identifier)] = dict(config)
        if auto_discover:
            self.discover_entrypoint_plugins()

    # ------------------------------------------------------------------
    # Discovery & registration
    # ------------------------------------------------------------------
    def discover_entrypoint_plugins(self) -> List[str]:
        """Discover and register plugins advertised via entry points."""
        discovered: List[str] = []
        for entry_point in self._iter_entry_points():
            try:
                plugin_cls = entry_point.load()
            except Exception as exc:
                logger.exception(
                    "Failed to import plugin from entry point %s: %s",
                    entry_point.name,
                    exc,
                )
                continue

            try:
                identifier = self.register_plugin(plugin_cls)
            except PluginDefinitionError as exc:
                logger.warning(
                    "Skipping invalid plugin %s from entry point %s: %s",
                    plugin_cls,
                    entry_point.name,
                    exc,
                )
                continue

            logger.info(
                "Discovered plugin '%s' from entry point '%s'", identifier, entry_point.name
            )
            discovered.append(identifier)

        return discovered

    def register_plugin(
        self,
        plugin_cls: Type[Plugin],
        *,
        name: Optional[str] = None,
    ) -> str:
        """Register a Plugin subclass for later usage."""
        if not inspect.isclass(plugin_cls) or not issubclass(plugin_cls, Plugin):
            raise PluginDefinitionError("Registered object must subclass Plugin")

        identifier = (name or plugin_cls.identifier()).strip()
        if not identifier:
            raise PluginDefinitionError(
                f"Plugin {plugin_cls.__name__} must define a non-empty identifier"
            )

        key = self._normalize(identifier)
        if key in self._registry:
            raise PluginDefinitionError(
                f"Plugin identifier '{identifier}' is already registered"
            )

        self._registry[key] = plugin_cls
        self._display_names[key] = identifier
        logger.debug("Registered plugin %s as '%s'", plugin_cls, identifier)
        return identifier

    def unregister_plugin(self, identifier: str) -> bool:
        """Remove a plugin registration. Does not teardown active instances."""
        key = self._normalize(identifier)
        removed = self._registry.pop(key, None) is not None
        self._display_names.pop(key, None)
        self._instances.pop(key, None)
        self._enabled.pop(key, None)
        return removed

    # ------------------------------------------------------------------
    # Enable / disable lifecycle
    # ------------------------------------------------------------------
    async def enable(self, identifier: str) -> Plugin:
        """Instantiate (if necessary) and run setup for a plugin."""
        key = self._normalize(identifier)
        plugin_cls = self._registry.get(key)
        if not plugin_cls:
            raise PluginLoadError(f"Plugin '{identifier}' is not registered")

        instance = self._instances.get(key)
        if instance is None:
            try:
                instance = plugin_cls(self.bot, config=self._configs.get(key))
            except Exception as exc:
                raise PluginLoadError(
                    f"Failed to instantiate plugin '{identifier}': {exc}"
                ) from exc
            self._instances[key] = instance

        if key in self._enabled:
            return instance

        if key in self._enabling_stack:
            raise PluginLoadError(
                f"Circular dependency detected while enabling '{identifier}'"
            )

        self._enabling_stack.add(key)
        try:
            await self._enable_dependencies(plugin_cls)
            await self._run_hook(instance.setup, identifier)
            self._enabled[key] = instance
            logger.info("Plugin '%s' enabled", self._display_names.get(key, identifier))
            return instance
        finally:
            self._enabling_stack.discard(key)

    async def enable_many(self, identifiers: Sequence[str]) -> List[Plugin]:
        enabled = []
        for identifier in identifiers:
            enabled.append(await self.enable(identifier))
        return enabled

    async def enable_all(self) -> List[Plugin]:
        return await self.enable_many(self.registered_plugins)

    async def disable(self, identifier: str) -> bool:
        """Run teardown for an enabled plugin."""
        key = self._normalize(identifier)
        instance = self._enabled.get(key)
        if not instance:
            return False

        await self._run_hook(instance.teardown, identifier)
        self._enabled.pop(key, None)
        logger.info("Plugin '%s' disabled", self._display_names.get(key, identifier))
        return True

    async def disable_all(self) -> None:
        for identifier in list(self._enabled.keys()):
            await self.disable(identifier)

    async def reload(self, identifier: str) -> Plugin:
        await self.disable(identifier)
        return await self.enable(identifier)

    # ------------------------------------------------------------------
    # Introspection helpers
    # ------------------------------------------------------------------
    @property
    def registered_plugins(self) -> List[str]:
        return list(self._display_names.values())

    @property
    def enabled_plugins(self) -> List[str]:
        return [self._display_names[key] for key in self._enabled]

    def get_instance(self, identifier: str) -> Optional[Plugin]:
        return self._enabled.get(self._normalize(identifier))

    def is_registered(self, identifier: str) -> bool:
        return self._normalize(identifier) in self._registry

    def is_enabled(self, identifier: str) -> bool:
        return self._normalize(identifier) in self._enabled

    def configure(self, identifier: str, config: Optional[Mapping[str, object]]) -> None:
        key = self._normalize(identifier)
        if config is None:
            self._configs.pop(key, None)
        else:
            self._configs[key] = dict(config)

        if key in self._instances:
            instance = self._instances[key]
            instance.config = instance._merge_config(config)  # type: ignore[attr-defined]

    def get_config(self, identifier: str) -> Optional[Mapping[str, object]]:
        return self._configs.get(self._normalize(identifier))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _normalize(self, identifier: str) -> str:
        return identifier.strip().lower()

    async def _enable_dependencies(self, plugin_cls: Type[Plugin]) -> None:
        dependencies = getattr(plugin_cls.meta, "dependencies", None) or ()
        for dep in dependencies:
            await self.enable(dep)

    async def _run_hook(self, hook, identifier: str) -> None:
        try:
            result = hook()
            if inspect.isawaitable(result):
                await result
        except Exception as exc:
            raise PluginLoadError(
                f"Plugin '{identifier}' hook execution failed: {exc}"
            ) from exc

    def _iter_entry_points(self) -> Iterable[importlib_metadata.EntryPoint]:
        try:
            entry_points = importlib_metadata.entry_points()
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.debug(
                "Failed to read entry points for plugin discovery: %s",
                exc,
            )
            return []

        if hasattr(entry_points, "select"):
            return entry_points.select(group=self.entry_point_group)

        return [
            entry_point
            for entry_point in entry_points
            if entry_point.group == self.entry_point_group
        ]
