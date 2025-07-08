import rubpy
from rubpy.types import Update

class GetSuggestedFolders:
    """
    Provides a method to get the suggested folders for the user.

    Methods:
    - get_suggested_folders: Get the suggested folders for the user.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def get_suggested_folders(
            self: "rubpy.Client"
    ) -> Update:
        """
        Get the suggested folders for the user.

        Returns:
        - rubpy.types.Update: The suggested folders for the user.
        """
        return await self.builder('getSuggestedFolders')  # type: ignore
