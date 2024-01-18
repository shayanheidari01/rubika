class LeaveGroupVoiceChat:
    async def leave_group_voice_chat(
            self,
            group_guid: str,
            voice_chat_id: str,
    ):
        return await self.builder('leaveGroupVoiceChat',
                                  input={
                                      'group_guid': group_guid,
                                      'voice_chat_id': voice_chat_id,
                                  })