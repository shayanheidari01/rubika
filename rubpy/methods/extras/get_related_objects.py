import rubpy

class GetRelatedObjects:
    async def get_related_objects(
            self: "rubpy.Client",
            object_guid: str,
    ):
        return await self.builder(
            name='getRelatedObjects',
            input=dict(object_guid=object_guid),
        )