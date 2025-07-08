import rubpy

class RemoveFromMyGifSet:
    async def remove_from_my_gif_set(
            self: "rubpy.Client",
            file_id: str,
    ) -> rubpy.types.Update:
        """
        Removes a GIF from the user's personal GIF set.

        Args:
            file_id (str): The file ID of the GIF to be removed.
        """
        return await self.builder('removeFromMyGifSet', input={'file_id': str(file_id)})
