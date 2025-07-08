import rubpy

class GetMyStickerSets:
    """
    Provides a method to get the sticker sets owned by the user.

    Methods:
    - get_my_sticker_sets: Get the sticker sets owned by the user.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def get_my_sticker_sets(self: "rubpy.Client") -> "rubpy.types.Update":
        """
        Get the sticker sets owned by the user.

        Returns:
        - The sticker sets owned by the user.
        """
        return await self.builder('getMyStickerSets')
