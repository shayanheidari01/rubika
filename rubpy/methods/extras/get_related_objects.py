import rubpy

class GetRelatedObjects:
    async def get_related_objects(
            self: "rubpy.Client",
            object_guid: str,
    ) -> rubpy.types.Update:
        """
        Get related objects for a given object.

        Args:
            object_guid (str): The GUID of the object.

        Returns:
            rubpy.types.Update: The update containing information about related objects.
        """
        return await self.builder(name='getRelatedObjects', input=dict(object_guid=object_guid))
