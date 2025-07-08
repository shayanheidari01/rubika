import rubpy
from rubpy.types import Update

class GetMySessions:
    """
    Provides a method to get information about the current user's sessions.

    Methods:
    - get_my_sessions: Get information about the current user's sessions.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def get_my_sessions(
            self: "rubpy.Client"
    ) -> Update:
        """
        Get information about the current user's sessions.

        Returns:
        - rubpy.types.Update: Information about the user's sessions.
        """
        return await self.builder('getMySessions')  # type: ignore
