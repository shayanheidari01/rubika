import rubpy
from rubpy.types import Update

class DeleteFolder:
    """
    Provides a method to delete a folder.

    Methods:
    - delete_folder: Delete a folder.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def delete_folder(
            self: "rubpy.Client",
            folder_id: str,
    ) -> Update:
        """
        Delete a folder.

        Parameters:
        - folder_id (str): The ID of the folder to be deleted.

        Returns:
        - rubpy.types.Update: Result of the delete folder operation.
        """
        return await self.builder(name='deleteFolder',
                                  input={'folder_id': str(folder_id)})  # type: ignore
