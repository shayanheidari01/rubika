import rubpy

class GetStickersByEmoji:
    """
    Provides a method to get stickers by emoji.

    Methods:
    - get_stickers_by_emoji: Get stickers by emoji.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def get_stickers_by_emoji(
            self: "rubpy.Client",
            emoji: str,
            suggest_by: str = 'All',
    ) -> "rubpy.types.Update":
        """
        Get stickers by emoji.

        Parameters:
        - emoji (str): The emoji character.
        - suggest_by (str): The type of suggestion (default is 'All').

        Returns:
        - Stickers corresponding to the provided emoji and suggestion type.
        """
        return await self.builder(
            name='getStickersByEmoji',
            input={'emoji_character': emoji, 'suggest_by': suggest_by}
        )
