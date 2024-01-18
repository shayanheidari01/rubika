from typing import Optional, Union
from time import time


class GetChatsUpdates:
    async def get_chats_updates(
            self,
            state: Optional[Union[str, int]] = None,
    ):
        if state is None:
            state = round(time()) - 150

        else:
            state = int(state)

        return await self.builder('getChatsUpdates',
                                  input={'state': state})