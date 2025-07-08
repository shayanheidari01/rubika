import rubpy
from typing import Literal

class SetBlockUser:
    async def set_block_user(
            self,
            user_guid: str,
            action: Literal['Block', 'Unblock'] = 'Block',
    ):
        if not action in ('Block', 'Unblock'):
            raise ValueError('`action` argument can only be `Block` or `Unblock`.')

        return await self.builder('setBlockUser',
                                  input={
                                      'user_guid': user_guid,
                                      'action': action,
                                  })