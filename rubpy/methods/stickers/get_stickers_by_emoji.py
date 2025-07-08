import rubpy

class GetStickersByEmoji:
    async def get_stickers_by_emoji(
            self: "rubpy.Client",
            emoji: str,
            suggest_by: str = 'All',
    ):
        return await self.builder(
            name='getStickersByEmoji',
            input={'emoji_character': emoji, 'suggest_by': suggest_by}
        )