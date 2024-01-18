class GetGroupLink:
    async def get_group_link(
            self,
            group_guid: str,
    ):
        return await self.builder('getGroupLink',
                                  input={
                                      'group_guid': group_guid,
                                  })