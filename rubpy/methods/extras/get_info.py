import rubpy

class GetInfo:
    async def get_info(
            self: "rubpy.Client",
            object_guid: str = None,
            username: str = None,
    ) -> rubpy.types.Update:
        """
        Get information about a user, group, or channel.

        Args:
            object_guid (str, optional): The GUID of the object (user, group, or channel).
            username (str, optional): The username of the object.

        Returns:
            rubpy.types.Update: The update containing information about the object.
        """
        if isinstance(object_guid, str):
            if object_guid.startswith('c0'):
                return await self.get_channel_info(object_guid)
            elif object_guid.startswith('u0'):
                return await self.get_user_info(object_guid)
            elif object_guid.startswith('g0'):
                return await self.get_group_info(object_guid)

        if isinstance(username, str):
            return await self.get_object_by_username(username)
