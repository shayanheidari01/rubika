import rubpy

class LeaveGroup:
    async def leave_group(
            self: "rubpy.Client",
            group_guid: str,
    ) -> rubpy.types.Update:
        """
        Leave a group.

        Args:
        - group_guid (str): The GUID of the group.

        Returns:
        - rubpy.types.Update: Update object confirming the leave group action.
        """
        return await self.builder('leaveGroup', input={'group_guid': group_guid})
