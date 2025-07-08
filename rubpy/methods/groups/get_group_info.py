import rubpy

class GetGroupInfo:
    async def get_group_info(
            self,
            group_guid: str,
    ) -> rubpy.types.Update:
        """
        Get information about a group.

        Args:
        - group_guid (str): The GUID of the group.

        Returns:
        - rubpy.types.Update: Update object containing information about the group.
        """
        return await self.builder('getGroupInfo',
                                  input={
                                      'group_guid': group_guid,
                                  })
