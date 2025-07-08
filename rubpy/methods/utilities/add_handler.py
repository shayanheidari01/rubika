import inspect
import rubpy
from rubpy import handlers
from typing import Callable, Union

class AddHandler:
    def add_handler(
            self: "rubpy.Client",
            func: Callable,
            handler: Union["handlers.ChatUpdates", "handlers.MessageUpdates", "handlers.ShowActivities", "handlers.ShowNotifications", "handlers.RemoveNotifications"],
    ) -> None:
        """
        Add a handler function for updates.

        Args:
        - func (Callable): The handler function to be added.
        - handler (rubpy.handlers.Handler): The handler object.

        Returns:
        - None
        """
        if not inspect.iscoroutinefunction(func):
            self.is_sync = True

        self.handlers[func] = handler
