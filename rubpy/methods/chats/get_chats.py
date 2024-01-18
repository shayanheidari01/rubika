from typing import Optional


class GetChats:
    async def get_chats(
            self,
            start_id: Optional[str]=None,
    ):
        return await self.builder('getChats',
                                  input={
                                      'start_id': start_id,
                                  })