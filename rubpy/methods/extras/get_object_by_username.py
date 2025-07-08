import rubpy

class GetObjectByUsername:
    async def get_object_by_username(
            self: "rubpy.Client",
            username: str,
    ) -> rubpy.types.Update:
        """
        Get an object (user, group, or channel) by its username.

        Args:
            username (str): The username of the object.

        Returns:
            rubpy.types.Update: The update containing information about the object.
        """
        username = username.replace('@', '')
        return await self.builder('getObjectByUsername',
                                  input={
                                      'username': username,
                                  })
