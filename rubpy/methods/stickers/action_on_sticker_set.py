import rubpy
from typing import Literal

class ActionOnStickerSet:
    """
    Provides a method to perform actions on a sticker set.

    Methods:
    - action_on_sticker_set: Add or remove a sticker set.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def action_on_sticker_set(
            self: "rubpy.Client",
            sticker_set_id: str,
            action: Literal['Add', 'Remove'] = 'Add',
    ) -> "rubpy.types.Update":
        """
        Add or remove a sticker set.

        Args:
        - sticker_set_id (str): The ID of the sticker set.
        - action (str, optional): The action to perform, either 'Add' or 'Remove'.

        Raises:
        - ValueError: If the action is not 'Add' or 'Remove'.

        Returns:
        - The result of the add/remove operation.
        """
        if action not in ('Add', 'Remove'):
            raise ValueError('The `action` argument can only be in `("Add", "Remove")`.')

        return await self.builder(name='actionOnStickerSet',
                                  input={
                                      'sticker_set_id': sticker_set_id,
                                      'action': action,
                                  })
