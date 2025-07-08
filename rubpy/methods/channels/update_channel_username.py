import rubpy
from rubpy.types import Update

class UpdateChannelUsername:
    async def update_channel_username(
            self: "rubpy.Client",
            channel_guid: str,
            username: str,
    ) -> Update:
        """
        Update the username of a channel.

        Parameters:
        - channel_guid (str): The unique identifier of the channel.
        - username (str): The new username for the channel.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        input = {
            'channel_guid': channel_guid,
            'username': username.replace('@', '')
        }

        return await self.builder(
            name='updateChannelUsername',
            input=input,
        )
