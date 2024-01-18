import rubpy

class DownloadProfilePicture:
    async def download_profile_picture(
            self: "rubpy.Client",
            object_guid: str,
    ):
        object = await self.get_info(object_guid)

        if object_guid.startswith('c0'):
            avatar_thumbnail = object.channel.avatar_thumbnail
        elif object_guid.startswith('g0'):
            avatar_thumbnail = object.group.avatar_thumbnail
        else:
            avatar_thumbnail = object.user.avatar_thumbnail

        if avatar_thumbnail:
            async with self.connection.session.get(
                url=f'https://messenger{avatar_thumbnail.dc_id}.iranlms.ir/InternFile.ashx',
                params={'id': avatar_thumbnail.file_id, 'ach': avatar_thumbnail.access_hash_rec},
            ) as response:
                if response.ok:
                    return await response.read()