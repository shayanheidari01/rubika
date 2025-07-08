import rubpy

class RemoveGroup:
    async def remove_group(
            self: "rubpy.Client",
            group_guid: str,
    ) -> rubpy.types.Update:
        """
        Remove a group.

        Args:
        - group_guid (str): The GUID of the group.

        Returns:
        - rubpy.types.Update: Update object confirming the removal of the group.
        """
        return await self.builder('removeGroup', input={'group_guid': group_guid})
