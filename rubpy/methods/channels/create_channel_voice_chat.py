import rubpy
from rubpy.types import Update

class CreateChannelVoiceChat:
    async def create_channel_voice_chat(
        self: "rubpy.Client",
        channel_guid: str,
    ) -> Update:
        """
        Create a voice chat for a channel.

        Parameters:
        - channel_guid (str): The GUID of the channel.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        return await self.builder('createChannelVoiceChat', input={'channel_guid': channel_guid})
