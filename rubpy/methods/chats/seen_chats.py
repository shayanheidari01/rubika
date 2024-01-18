class SeenChats:
    async def seen_chats(
            self,
            seen_list: dict,
    ):
        return await self.builder('seenChats',
                                  input={
                                      'seen_list': seen_list,
                                  })