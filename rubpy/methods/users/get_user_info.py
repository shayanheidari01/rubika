import rubpy

class GetUserInfo:
    """
    Provides a method to get information about a user.

    Methods:
    - get_user_info: Get information about a specific user.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def get_user_info(
            self: "rubpy.Client",
            user_guid: str=None,
    ) -> "rubpy.types.Update":
        """
        Get information about a specific user.

        Args:
        - user_guid (str, optional): The GUID of the user to get information about.

        Returns:
        - Information about the specified user.
        """
        result = await self.builder(
            name='getUserInfo',
            input={} if user_guid is None else {'user_guid': user_guid},
            tmp_session=True if self.auth is None else False,
        )
        return result
