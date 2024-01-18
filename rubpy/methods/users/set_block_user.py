class SetBlockUser:
    async def set_block_user(
            self,
            user_guid: str,
            action: str = 'Block',
    ):
        if not action in ():
            raise ValueError('`action` argument can only be `Block` or `Unblock`.')

        return await self.builder('setBlockUser',
                                  input={
                                      'user_guid': user_guid,
                                      'action': action,
                                  })