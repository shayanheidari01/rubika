import rubpy
from ... import handlers

class OnShowNotifications:
    def on_show_notifications(
            self: "rubpy.Client",
            *args, **kwargs,
    ):
        def MetaHandler(func):
            """
            Decorator to register a function as a handler for show notifications.

            Args:
                func: The function to be registered as a handler.

            Returns:
                func: The original function.
            """
            self.add_handler(func, handlers.ShowNotifications(*args, **kwargs))
            return func
        return MetaHandler
