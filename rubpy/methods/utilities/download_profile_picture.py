import rubpy

class DownloadProfilePicture:
    async def download_profile_picture(
            self: "rubpy.Client",
            object_guid: str,
    ) -> bytes:
        """
        Download the profile picture of a user, group, or channel.

        Args:
        - object_guid (str): The GUID of the user, group, or channel.

        Returns:
        - bytes: The binary data of the profile picture.

        Raises:
        - rubpy.errors.ApiError: If there is an issue with the Rubpy API.
        """
        object_info = await self.get_info(object_guid)

        if object_guid.startswith('c0'):
            avatar_thumbnail = object_info.channel.avatar_thumbnail
        elif object_guid.startswith('g0'):
            avatar_thumbnail = object_info.group.avatar_thumbnail
        else:
            avatar_thumbnail = object_info.user.avatar_thumbnail

        if avatar_thumbnail:
            async with self.connection.session.get(
                url=f'https://messenger{avatar_thumbnail.dc_id}.iranlms.ir/InternFile.ashx',
                params={'id': avatar_thumbnail.file_id, 'ach': avatar_thumbnail.access_hash_rec},
            ) as response:
                if response.ok:
                    return await response.read()
        return bytes()  # Return an empty bytes object if no profile picture is found.
