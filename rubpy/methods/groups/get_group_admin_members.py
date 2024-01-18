class GetGroupAdminMembers:
    async def get_group_admin_members(
            self,
            group_guid: str,
            start_id: str=None,
    ):
        return await self.builder('getGroupAdminMembers',
                                  input={
                                      'group_guid': group_guid,
                                      'start_id': start_id,
                                  })