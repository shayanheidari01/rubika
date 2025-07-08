import rubpy

class GetPollStatus:
    """
    Provides a method to get the status of a specific poll.

    Methods:
    - get_poll_status: Get the status of a specific poll.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def get_poll_status(
            self: "rubpy.Client",
            poll_id: str,
    ) -> rubpy.types.Update:
        """
        Get the status of a specific poll.

        Parameters:
        - poll_id (str): The ID of the poll for which the status is requested.

        Returns:
        - rubpy.types.Update: The status of the specified poll.
        """
        return self.builder(name='getPollStatus',
                            input={
                                'poll_id': poll_id,
                            })
