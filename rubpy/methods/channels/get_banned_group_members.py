class GetBannedGroupMembers:
    async def get_banned_group_members(
            self,
            group_guid: str,
            start_id: str=None,
    ):
        return await self.builder('getBannedGroupMembers',
                                  input={
                                      'group_guid': group_guid,
                                      'start_id': start_id,
                                  })