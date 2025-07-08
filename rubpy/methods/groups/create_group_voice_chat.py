import rubpy

class CreateGroupVoiceChat:
    async def create_group_voice_chat(
            self: "rubpy.Client",
            group_guid: str,
    ) -> rubpy.types.Update:
        """
        Create a voice chat in a group.

        Args:
        - group_guid (str): The GUID of the group.

        Returns:
        - rubpy.types.Update: The result of the API call.
        """
        return await self.builder('createGroupVoiceChat',
                                  input={
                                      'group_guid': group_guid,
                                  })
