import rubpy
from rubpy.types import Update

class GetChannelInfo:
    async def get_channel_info(
            self: "rubpy.Client",
            channel_guid: str,
    ) -> Update:
        """
        Get information about a channel.

        Parameters:
        - channel_guid (str): The GUID of the channel.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        return await self.builder('getChannelInfo', input={'channel_guid': channel_guid})
