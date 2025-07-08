import rubpy
from rubpy.types import Update

class RemoveChannel:
    async def remove_channel(
            self: "rubpy.Client",
            channel_guid: str,
    ) -> Update:
        """
        Remove a channel.

        Parameters:
        - channel_guid (str): The unique identifier of the channel.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        return await self.builder('removeChannel',
                                  input={
                                      'channel_guid': channel_guid,
                                  })
