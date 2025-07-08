from typing import Union
from time import time
import rubpy
from rubpy.types import Update

class GetFolders:
    """
    Provides a method to get a list of folders.

    Methods:
    - get_folders: Get a list of folders.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def get_folders(
            self: "rubpy.Client",
            last_state: Union[int, str] = round(time()) - 150
    ) -> Update:
        """
        Get a list of folders.

        Parameters:
        - last_state (Union[int, str]): The last state to retrieve folders.

        Returns:
        - rubpy.types.Update: List of folders.
        """
        return await self.builder(name='getFolders',
                                  input={'last_state': int(last_state)})  # type: ignore
