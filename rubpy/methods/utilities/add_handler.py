import inspect

class AddHandler:
    def add_handler(self, func, handler):
        if not inspect.iscoroutinefunction(func):
            self.is_sync = True

        self.handlers[func] = handler