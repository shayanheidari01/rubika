class DeleteNoAccessGroupChat:
    async def delete_no_access_group_chat(
            self,
            group_guid: str,
    ):
        return await self.builder('deleteNoAccessGroupChat',
                                  input={
                                      'group_guid': group_guid,
                                  })