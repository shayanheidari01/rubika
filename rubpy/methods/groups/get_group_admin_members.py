import rubpy

class GetGroupAdminMembers:
    async def get_group_admin_members(
            self: "rubpy.Client",
            group_guid: str,
            start_id: str=None,
    ) -> rubpy.types.Update:
        """
        Get the list of admin members in a group.

        Args:
        - group_guid (str): The GUID of the group.
        - start_id (str, optional): The starting ID for pagination. Defaults to None.

        Returns:
        - rubpy.types.Update: The result of the API call.
        """
        return await self.builder('getGroupAdminMembers',
                                  input={
                                      'group_guid': group_guid,
                                      'start_id': start_id,
                                  })
