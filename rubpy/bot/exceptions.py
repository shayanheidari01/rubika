class APIException(Exception):
    """
    Exception for handling Rubika API errors.

    Attributes:
        status (str): Response status from API.
        dev_message (str): Optional developer message from API.
    """

    def __init__(self, status: str, dev_message: str = None):
        self.status = status
        self.dev_message = dev_message
        super().__init__(self.__str__())

    def __str__(self):
        if self.dev_message:
            return f"RubikaAPIError: status={self.status}, dev_message={self.dev_message}"
        return f"RubikaAPIError: status={self.status}"
