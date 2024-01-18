class SetActionChat:
    async def set_action_chat(
            self,
            object_guid: str,
            action: str='Mute',
    ):
        if action not in ('Mute', 'Unmute'):
            raise ValueError('`action` argument can only be `Mute` or `Unmute`.')
    
        return await self.builder('setActionChat',
                                  input={
                                      'object_guid': object_guid,
                                      'action': action,
                                  })