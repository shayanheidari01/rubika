import rubpy

class GetTrendStickerSets:
    async def get_trend_sticker_sets(
            self: "rubpy.Client",
            start_id: str = None,
    ):
        return await self.builder(name='getTrendStickerSets',
                                  input={'start_id': str(start_id)})