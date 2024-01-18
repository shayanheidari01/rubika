from typing import Union
from time import time
import rubpy

class GetFolders:
    async def get_folders(
            self: "rubpy.Client",
            last_state: Union[int, str] = round(time()) - 150,
    ):
        return await self.builder(name='getFolders',
                                  input={'last_state': int(last_state)})