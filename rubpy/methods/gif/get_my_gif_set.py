import rubpy


class GetMyGifSet:
    async def get_my_gif_set(self: "rubpy.Client"):
        return await self.builder('getMyGifSet')