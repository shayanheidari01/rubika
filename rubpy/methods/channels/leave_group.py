class LeaveGroup:
    async def leave_group(
            self,
            group_guid: str,
    ):
        return await self.builder('leaveGroup',
                                  input={
                                      'group_guid': group_guid,
                                  })