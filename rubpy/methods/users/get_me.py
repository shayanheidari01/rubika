import rubpy

class GetMe:
    """
    Provides a method to get information about the authenticated user.

    Methods:
    - get_me: Get information about the authenticated user.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def get_me(self: "rubpy.Client") -> "rubpy.types.Update":
        """
        Get information about the authenticated user.

        Returns:
        - Information about the authenticated user.
        """
        return await self.get_user_info()
