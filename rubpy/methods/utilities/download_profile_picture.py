import rubpy

class DownloadProfilePicture:
    async def download_profile_picture(
            self: "rubpy.Client",
            object_guid: str,
    ) -> bytes:
        """
        Download the profile picture of a user, group, or channel.

        Args:
        - object_guid (str): The GUID of the user, group, channel or other chats.

        Returns:
        - bytes: The binary data of the profile picture.

        Raises:
        - rubpy.errors.ApiError: If there is an issue with the Rubpy API.
        """
        avatars = await self.get_avatars(object_guid)

        if avatars:
            avatars = avatars.avatars[0].main
            async with self.connection.session.get(
                url=f'https://messenger{avatars.dc_id}.iranlms.ir/InternFile.ashx',
                params={'id': avatars.file_id, 'ach': avatars.access_hash_rec},
            ) as response:
                if response.ok:
                    return await response.read()

        return bytes()  # Return an empty bytes object if no profile picture is found.