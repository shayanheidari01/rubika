import rubpy

class GetGroupAdminAccessList:
    async def get_group_admin_access_list(
            self: "rubpy.Client",
            group_guid: str,
            member_guid: str,
    ) -> rubpy.types.Update:
        """
        Get the admin access list for a member in a group.

        Args:
        - group_guid (str): The GUID of the group.
        - member_guid (str): The GUID of the member for whom admin access is being checked.

        Returns:
        - rubpy.types.Update: The result of the API call.
        """
        return await self.builder('getGroupAdminAccessList',
                                  input={
                                      'group_guid': group_guid,
                                      'member_guid': member_guid,
                                  })
