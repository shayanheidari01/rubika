import rubpy

class RemoveFromMyGifSet:
    async def remove_from_my_gif_set(
            self: "rubpy.Client",
            file_id: str,
    ):
        return await self.builder('removeFromMyGifSet', input={'file_id': str(file_id)})