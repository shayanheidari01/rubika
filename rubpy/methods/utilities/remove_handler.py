import rubpy

class RemoveHandler:
    def remove_handler(self: "rubpy.Client", func) -> None:
        """
        Remove a handler function.

        Args:
        - func: The handler function to be removed.
        """
        try:
            self.handlers.pop(func)

        except KeyError:
            pass