import rubpy

class GetStickerSetByID:
    async def get_sticker_set_by_id(
            self: "rubpy.Client",
            sticker_set_id: str,
    ):
        return await self.builder(
            name='getStickerSetByID',
            input={'sticker_set_id': str(sticker_set_id)}
        )