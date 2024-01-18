class GetGroupDefaultAccess:
    async def get_group_default_access(
            self,
            group_guid: str,
    ):
        return await self.builder('getGroupDefaultAccess',
                                  input={
                                      'group_guid': group_guid,
                                  })