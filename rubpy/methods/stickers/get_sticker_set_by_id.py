import rubpy

class GetStickerSetByID:
    """
    Provides a method to get a sticker set by its ID.

    Methods:
    - get_sticker_set_by_id: Get a sticker set by its ID.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def get_sticker_set_by_id(
            self: "rubpy.Client",
            sticker_set_id: str,
    ) -> "rubpy.types.Update":
        """
        Get a sticker set by its ID.

        Parameters:
        - sticker_set_id (str): The ID of the sticker set.

        Returns:
        - The sticker set corresponding to the provided ID.
        """
        return await self.builder(
            name='getStickerSetByID',
            input={'sticker_set_id': str(sticker_set_id)}
        )
