import rubpy

class SetGroupVoiceChatSetting:
    async def set_group_voice_chat_setting(
            self: "rubpy.Client",
            group_guid: str,
            voice_chat_id: str,
            title: str=None,
    ) -> rubpy.types.Update:
        """
        Set group voice chat setting.

        Args:
        - group_guid (str): The GUID of the group.
        - voice_chat_id (str): The voice chat ID.
        - title (str): Title of voice chat, Defualt is None.

        Returns:
        - rubpy.types.Update: Update object confirming the change in default access.
        """
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