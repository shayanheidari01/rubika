import rubpy
from pathlib import Path
from typing import Union

class UploadAvatar:
    async def upload_avatar(
            self: "rubpy.Client",
            object_guid: str,
            image: Union[Path, bytes], *args, **kwargs,
    ):
        """
        Uploads an avatar image for a specified object (user, group, or chat).

        Args:
            object_guid (str): The GUID of the object for which the avatar is being uploaded.
            image (Union[Path, bytes]): The image file or bytes to be used as the avatar.
            *args, **kwargs: Additional arguments to be passed to the `upload` method.

        Returns:
            rubpy.types.Update: The result of the avatar upload operation.

        Raises:
            Any exceptions that might occur during the avatar upload process.

        Note:
            - If `object_guid` is 'me', 'cloud', or 'self', it will be replaced with the client's GUID.
            - If `image` is a string (path to a file), the file name is extracted from the path.
              Otherwise, a default file name ('rubpy.jpg') is used.
            - The `upload` method is used internally to handle the file upload process.
        """
        if object_guid.lower() in ('me', 'cloud', 'self'):
            object_guid = self.guid

        if isinstance(image, str):
            kwargs['file_name'] = kwargs.get('file_name', image.split('/')[-1])
        else:
            kwargs['file_name'] = kwargs.get('file_name', 'rubpy.jpg')

        upload = await self.upload(image, *args, **kwargs)

        input = dict(
            object_guid=object_guid,
            thumbnail_file_id=upload.file_id,
            main_file_id=upload.file_id,
        )

        return await self.builder(name='uploadAvatar', input=input)
