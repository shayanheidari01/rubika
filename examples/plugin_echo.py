"""Practical example of creating and enabling a Rubpy plugin inline.

Usage:
    export RUBPY_BOT_TOKEN="..."
    python examples/plugin_echo.py

The EchoPlugin registers a handler that mirrors received private texts.
"""

from __future__ import annotations

import asyncio
import os
from typing import Optional

from rubpy.bot import BotClient, filters
from rubpy.bot.models import Update
from rubpy.plugins import Plugin, PluginMeta


class LoggerPlugin(Plugin):
    """Simple middleware plugin used as a dependency example."""

    meta = PluginMeta(
        name="examples.logger",
        version="1.0.0",
        description="Logs every text update that passes through.",
        author="Rubpy Team",
        homepage="https://github.com/shayanheidari01/rubika",
        default_config={"log_prefix": "[LOGGER]"},
    )

    def setup(self):
        prefix = self.get_config("log_prefix", "[LOGGER]")

        @self.bot.middleware()
        async def log_updates(bot: BotClient, update: Update, call_next):
            text = getattr(update.new_message, "text", None)
            if text:
                print(f"{prefix} chat={update.chat_id} text={text}")
            await call_next()


class EchoPlugin(Plugin):
    """Demonstrates dependency + configuration overrides."""

    meta = PluginMeta(
        name="examples.echo",
        version="1.1.0",
        description="Echo private messages back to the sender.",
        author="Rubpy Team",
        homepage="https://github.com/shayanheidari01/rubika",
        dependencies=(LoggerPlugin.meta.name,),
        default_config={
            "prefix": "Echo",
            "upper": False,
        },
    )

    def setup(self):
        prefix = self.get_config("prefix", "Echo")
        make_upper = bool(self.get_config("upper", False))

        @self.bot.on_update(filters.private & filters.text)
        async def echo_text(client: BotClient, update: Update):
            text: Optional[str] = (
                getattr(update.new_message, "text", None)
                if update.new_message
                else None
            )
            if text:
                payload = text.upper() if make_upper else text
                await client.send_message(update.chat_id, f"{prefix}: {payload}")


async def main() -> None:
    token = os.environ.get("RUBPY_BOT_TOKEN")
    if not token:
        raise SystemExit("Please export RUBPY_BOT_TOKEN before running this example.")

    bot = BotClient(
        token,
        auto_enable_plugins=True,
        plugins=[EchoPlugin.meta.name],
        plugin_configs={
            LoggerPlugin.meta.name: {"log_prefix": "[EchoDemo]"},
            EchoPlugin.meta.name: {"prefix": "🔥 Echo", "upper": True},
        },
    )

    # Register the plugin classes dynamically (as if installed via PyPI)
    bot.register_plugin(LoggerPlugin)
    bot.register_plugin(EchoPlugin)

    try:
        print("Bot starting... Press Ctrl+C to stop.")
        await bot.run()
    except KeyboardInterrupt:
        print("Stopping bot...")


if __name__ == "__main__":
    asyncio.run(main())
