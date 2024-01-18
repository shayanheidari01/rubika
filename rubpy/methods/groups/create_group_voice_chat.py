class CreateGroupVoiceChat:
    async def create_group_voice_chat(
            self,
            group_guid: str,
    ):
        return await self.builder('createGroupVoiceChat',
                                  input={
                                      'group_guid': group_guid,
                                  })