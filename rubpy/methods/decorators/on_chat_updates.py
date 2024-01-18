import rubpy
from ... import handlers


class OnChatUpdates:
    def on_chat_updates(
            self: "rubpy.Client",
            *args, **kwargs,
    ):
        def MetaHandler(func):
            self.add_handler(func, handlers.ChatUpdates(*args, **kwargs))
            return func
        return MetaHandler