class SetGroupVoiceChatSetting:
    async def set_group_voice_chat_setting(
            self,
            group_guid: str,
            voice_chat_id: str,
            title: str=None,
    ):
        input = {
            'group_guid': group_guid,
            'voice_chat_id': voice_chat_id,
        }
        updated_parameters = []

        if title is not None:
            input['title'] = title
            updated_parameters.append('title')

        return await self.builder('setGroupVoiceChatSetting',
                                  input=input)