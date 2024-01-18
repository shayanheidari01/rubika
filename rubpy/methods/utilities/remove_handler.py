class RemoveHandler:
    def remove_handler(self, func):
        try:
            self.handlers.pop(func)
        except KeyError:
            pass