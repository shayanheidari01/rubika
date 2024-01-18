class RemoveGroup:
    async def remove_group(
            self,
            group_guid: str,
    ):
        return await self.builder('removeGroup',
                                  input={
                                      'group_guid': group_guid,
                                  })