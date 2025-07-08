import rubpy
from rubpy.types import Update

class GetBlockedUsers:
    """
    Provides a method to get a list of blocked users.

    Methods:
    - get_blocked_users: Get a list of blocked users.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def get_blocked_users(
            self: "rubpy.Client"
    ) -> Update:
        """
        Get a list of blocked users.

        Returns:
        - rubpy.types.Update: List of blocked users.
        """
        return await self.builder('getBlockedUsers')  # type: ignore
