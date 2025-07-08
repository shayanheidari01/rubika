import rubpy
from ... import handlers

class OnShowActivities:
    def on_show_activities(
            self: "rubpy.Client",
            *args, **kwargs,
    ):
        def MetaHandler(func):
            """
            Decorator to register a function as a handler for show activities.

            Args:
                func: The function to be registered as a handler.

            Returns:
                func: The original function.
            """
            self.add_handler(func, handlers.ShowActivities(*args, **kwargs))
            return func
        return MetaHandler
