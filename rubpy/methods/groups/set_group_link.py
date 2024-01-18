class SetGroupLink:
    async def set_group_link(
            self,
            group_guid: str,
    ):
        return await self.builder('setGroupLink',
                                  input={
                                      'group_guid': group_guid,
                                  })