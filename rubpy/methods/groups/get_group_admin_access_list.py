class GetGroupAdminAccessList:
    async def get_group_admin_access_list(
            self,
            group_guid: str,
            member_guid: str,
    ):
        return await self.builder('getGroupAdminAccessList',
                                  input={
                                      'group_guid': group_guid,
                                      'member_guid': member_guid,
                                  })