import rubpy

class SetChannelVoiceChatSetting:
    async def set_channel_voice_chat_setting(
            self: "rubpy.Client",
            channel_guid: str,
            voice_chat_id: str,
            title: str=None,
    ):
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