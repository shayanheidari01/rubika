import rubpy


class GetMessages:
    async def get_messages(
        self: "rubpy.Client",
        object_guid: str,
        max_id: str,
        limit: str,
        sort: str = "FromMax",
    ):
        input: dict = {
            "object_guid": object_guid,
            "sort": sort,
            "max_id": max_id,
            "limit": limit,
        }
        return await self.builder("getMessages", input=input)
