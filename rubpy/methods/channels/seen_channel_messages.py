import rubpy
from typing import Union
from rubpy.types import Update

class SeenChannelMessages:
    async def seen_channel_messages(
            self: "rubpy.Client",
            channel_guid: str,
            min_id: Union[int, str],
            max_id: Union[int, str],
    ) -> Update:
        """
        Mark channel messages as seen within a specific range.

        Parameters:
        - channel_guid (str): The unique identifier of the channel.
        - min_id (Union[int, str]): The minimum message ID to mark as seen.
        - max_id (Union[int, str]): The maximum message ID to mark as seen.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        data = dict(
            channel_guid=channel_guid,
            min_id=min_id,
            max_id=max_id,
        )
        return await self.builder(
            name='seenChannelMessages',
            input=data,
        )
