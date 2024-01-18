import rubpy


class AddToMyGifSet:
    async def add_to_my_gif_set(
            self: "rubpy.Client",
            object_guid: str,
            message_id: str,
    ):
        input = dict(
            object_guid=object_guid,
            message_id=message_id,
        )

        return await self.builder('addToMyGifSet', input=input)