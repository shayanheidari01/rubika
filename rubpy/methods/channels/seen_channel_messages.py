import rubpy
from typing import Union

class SeenChannelMessages:
    async def seen_channel_messages(
            self: "rubpy.Client",
            channel_guid: str,
            min_id: Union[int, str],
            max_id: Union[int, str],
    ):
        data = dict(
            channel_guid=channel_guid,
            min_id=min_id,
            max_id=max_id,
        )
        return await self.builder(
            name='seenChannelMessages',
            input=data,
        )