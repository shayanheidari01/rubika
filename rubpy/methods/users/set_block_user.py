import rubpy
from typing import Literal

class SetBlockUser:
    """
    Provides a method to block or unblock a user.

    Methods:
    - set_block_user: Block or unblock a user.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def set_block_user(
            self: "rubpy.Client",
            user_guid: str,
            action: Literal['Block', 'Unblock'] = 'Block',
    ) -> "rubpy.types.Update":
        """
        Block or unblock a user.

        Args:
        - user_guid (str): The GUID of the user to block or unblock.
        - action (Literal['Block', 'Unblock'], optional): The action to perform, either 'Block' or 'Unblock'.

        Raises:
        - ValueError: If the action is not 'Block' or 'Unblock'.

        Returns:
        - The result of the block/unblock operation.
        """
        if not action in ('Block', 'Unblock'):
            raise ValueError('`action` argument can only be `Block` or `Unblock`.')

        return await self.builder('setBlockUser',
                                  input={
                                      'user_guid': user_guid,
                                      'action': action,
                                  })
