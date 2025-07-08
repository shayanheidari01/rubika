import rubpy
from rubpy.types import Update

class SetChannelLink:
    async def set_channel_link(
            self: "rubpy.Client",
            channel_guid: str,
    ) -> Update:
        """
        Set a custom link for the channel.

        Parameters:
        - channel_guid (str): The unique identifier of the channel.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        return await self.builder('setChannelLink',
                                  input={
                                      'channel_guid': channel_guid,
                                  })
