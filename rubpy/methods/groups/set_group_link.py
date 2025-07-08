import rubpy

class SetGroupLink:
    async def set_group_link(
            self: "rubpy.Client",
            group_guid: str,
    ) -> rubpy.types.Update:
        """
        Set private link for group.

        Args:
        - group_guid (str): The GUID of the group.

        Returns:
        - rubpy.types.Update: Update object confirming the change in default access.
        """
        return await self.builder('setGroupLink',
                                  input={
                                      'group_guid': group_guid,
                                  })