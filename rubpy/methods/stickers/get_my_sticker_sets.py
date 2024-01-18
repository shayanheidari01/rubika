import rubpy

class GetMyStickerSets:
    async def get_my_sticker_sets(self: "rubpy.Client"):
        return await self.builder('getMyStickerSets')