import rubpy
from rubpy.types import Update

class GetAvatars:
    async def get_avatars(
            self: "rubpy.Client",
            object_guid: str,
    ) -> Update:
        """
        Get avatars of a specific object.

        Parameters:
        - object_guid (str): The unique identifier of the object to retrieve avatars for.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        return await self.builder('getAvatars',
                                  input={
                                      'object_guid': object_guid,
                                  })
