import rubpy
from rubpy.types import Update

class SetChannelVoiceChatSetting:
    async def set_channel_voice_chat_setting(
            self: "rubpy.Client",
            channel_guid: str,
            voice_chat_id: str,
            title: str=None,
    ) -> Update:
        """
        Set the title for a voice chat in a channel.

        Parameters:
        - channel_guid (str): The unique identifier of the channel.
        - voice_chat_id (str): The unique identifier of the voice chat.
        - title (str, optional): The new title for the voice chat.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        input = {
            'channel_guid': channel_guid,
            'voice_chat_id': voice_chat_id,
        }
        updated_parameters = []

        if title is not None:
            input['title'] = title
            updated_parameters.append('title')

        return await self.builder('setChannelVoiceChatSetting',
                                  input=input)
