import rubpy


class CheckUserUsername:
    """
    Provides a method to check the availability of a username for a user.

    Methods:
    - check_user_username: Check the availability of a username.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def check_user_username(self: "rubpy.Client", username: str) -> "rubpy.types.Update":
        """
        Check the availability of a username for a user.

        Args:
        - username (str): The username to be checked.

        Returns:
        - The result of the username availability check.
        """
        return await self.builder('checkUserUsername', input=dict(username=username))
