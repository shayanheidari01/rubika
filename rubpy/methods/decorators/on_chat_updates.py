import rubpy
from ... import handlers

class OnChatUpdates:
    def on_chat_updates(
            self: "rubpy.Client",
            *args, **kwargs,
    ):
        def MetaHandler(func):
            """
            Decorator to register a function as a handler for chat updates.

            Args:
                func: The function to be registered as a handler.

            Returns:
                func: The original function.
            """
            self.add_handler(func, handlers.ChatUpdates(*args, **kwargs))
            return func
        return MetaHandler
