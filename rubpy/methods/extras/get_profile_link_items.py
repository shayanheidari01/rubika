import rubpy

class GetProfileLinkItems:
    async def get_profile_link_items(
            self: "rubpy.Client",
            object_guid: str,
    ) -> rubpy.types.Update:
        """
        Get profile link items for a given object.

        Args:
            object_guid (str): The GUID of the object.

        Returns:
            rubpy.types.Update: The update containing information about profile link items.
        """
        return await self.builder('getProfileLinkItems', input=dict(object_guid=object_guid))
