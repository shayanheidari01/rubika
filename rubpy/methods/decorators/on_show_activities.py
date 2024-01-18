import rubpy
from ... import handlers


class OnShowActivities:
    def on_show_activities(
            self: "rubpy.Client",
            *args, **kwargs,
    ):
        def MetaHandler(func):
            self.add_handler(func, handlers.ShowActivities(*args, **kwargs))
            return func
        return MetaHandler