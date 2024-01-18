class SendChatActivity:
    async def send_chat_activity(
            self,
            object_guid: str,
            activity: str = 'Typing',
    ):
        if activity not in ('Typing', 'Uploading', 'Recording'):
            raise ValueError('`activity` argument can only be in `["Typing", "Uploading", "Recording"]`')
    
        return await self.builder('sendChatActivity',
                                  input={
                                      'object_guid': object_guid,
                                      'activity': activity,
                                  })