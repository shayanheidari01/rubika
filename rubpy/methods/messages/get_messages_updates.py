import rubpy
from time import time


class GetMessagesUpdates:
    async def get_messages_updates(
            self: "rubpy.Client",
            object_guid: str,
            state: int = round(time()) - 150,
    ):
        return await self.builder('getMessagesUpdates',
                                  input=dict(
                                      object_guid=object_guid,
                                      state=int(state),
                                  ))