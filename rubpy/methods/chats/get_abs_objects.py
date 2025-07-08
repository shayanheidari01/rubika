import rubpy
from rubpy.types import Update
from typing import Union

class GetAbsObjects:
    async def get_abs_objects(
            self,
            object_guids: Union[str, list],
    ) -> Update:
        """
        Get absolute objects based on their unique identifiers.

        Parameters:
        - object_guids (Union[str, list]): The unique identifiers of the objects to retrieve.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        if isinstance(object_guids, str):
            object_guids = list(object_guids)

        return await self.builder('getAbsObjects',
                                  input={
                                      'object_guids': object_guids,
                                  })
