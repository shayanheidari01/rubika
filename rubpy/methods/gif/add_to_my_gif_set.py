import rubpy

class AddToMyGifSet:
    async def add_to_my_gif_set(
            self: "rubpy.Client",
            object_guid: str,
            message_id: str,
    ) -> rubpy.types.Update:
        """
        Adds a GIF message to the user's personal GIF set.

        Args:
            object_guid (str): The GUID of the chat or channel.
            message_id (str): The ID of the GIF message.
        """
        input_data = {
            'object_guid': object_guid,
            'message_id': message_id,
        }

        return await self.builder('addToMyGifSet', input=input_data)
