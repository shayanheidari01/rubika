import rubpy

class GetMyGifSet:
    async def get_my_gif_set(
            self: "rubpy.Client"
    ) -> rubpy.types.Update:
        """
        Gets the user's personal GIF set.

        Returns:
            rubpy.types.Update: Information about the user's GIF set.
        """
        return await self.builder('getMyGifSet')
