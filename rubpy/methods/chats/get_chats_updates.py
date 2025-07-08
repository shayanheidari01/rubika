import rubpy
from typing import Optional, Union
from time import time
from rubpy.types import Update

class GetChatsUpdates:
    async def get_chats_updates(
            self: "rubpy.Client",
            state: Optional[Union[str, int]] = None,
    ) -> Update:
        """
        Get updates for chats.

        Parameters:
        - state (Optional[Union[str, int]]): State parameter for syncing updates. If not provided,
          it uses the current time minus 150 seconds.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        return await self.builder('getChatsUpdates',
                                  input={'state': round(time()) - 150 if state is None else int(state)})
