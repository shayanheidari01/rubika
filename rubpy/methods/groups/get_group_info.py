class GetGroupInfo:
    async def get_group_info(
            self,
            group_guid: str,
    ):
        return await self.builder('getGroupInfo',
                                  input={
                                      'group_guid': group_guid,
                                  })