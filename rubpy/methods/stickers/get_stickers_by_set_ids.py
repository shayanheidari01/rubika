from typing import Union
import rubpy

class GetStickersBySetIDs:
    """
    Provides a method to get stickers by set IDs.

    Methods:
    - get_stickers_by_set_ids: Get stickers by set IDs.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def get_stickers_by_set_ids(
            self: "rubpy.Client",
            sticker_set_ids: Union[str, list],
    ) -> rubpy.types.Update:
        """
        Get stickers by set IDs.

        Parameters:
        - sticker_set_ids (Union[str, list]): The sticker set ID or a list of sticker set IDs.

        Returns:
        - Stickers corresponding to the provided set IDs.
        """
        if isinstance(sticker_set_ids, str):
            sticker_set_ids = [str(sticker_set_ids)]

        return await self.builder(name='GetStickersBySetIDs',
                                  input={'sticker_set_ids': sticker_set_ids})