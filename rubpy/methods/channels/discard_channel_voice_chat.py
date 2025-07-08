import rubpy
from rubpy.types import Update

class DiscardChannelVoiceChat:
    async def discard_channel_voice_chat(
        self: "rubpy.Client",
        channel_guid: str,
        voice_chat_id: str,
    ) -> Update:
        """
        Discard a voice chat in a channel.

        Parameters:
        - channel_guid (str): The GUID of the channel.
        - voice_chat_id (str): The ID of the voice chat to discard.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        return await self.builder(
            name='discardChannelVoiceChat',
            input={
                'channel_guid': channel_guid,
                'voice_chat_id': voice_chat_id,
            }
        )
