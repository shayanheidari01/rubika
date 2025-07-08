from ...types import Results
from ..utilities import thumbnail
from typing import Optional, Union
from aiofiles import open as aiopen
from asyncio import create_task
from pathlib import Path
from os import path
from random import random
import rubpy
import aiohttp


class SendMessage:
    async def send_message(self: "rubpy.Client",
                           object_guid: str,
                           text: Optional[str] = None,
                           reply_to_message_id: Optional[str] = None,
                           file_inline: Optional[Union[Path, bytes]] = None,
                           sticker: Optional[dict] = None,
                           type: str = 'File',
                           is_spoil: bool = False,
                           thumb: bool = True,
                           auto_delete: Optional[int] = None,
                           parse_mode: Optional[str] = None, *args, **kwargs):
        """_send message_

        Args:
            object_guid (str):
                _object guid_

            message (Any, optional):
                _message or cation or sticker_ . Defaults to None.

            reply_to_message_id (str, optional):
                _reply to message id_. Defaults to None.

            file_inline (typing.Union[pathlib.Path, bytes], optional):
                _file_. Defaults to None.

            type (str, optional):
                _file type_. Defaults to methods.messages.File.(
                    methods.messages.Gif,
                    methods.messages.Image,
                    methods.messages.Voice,
                    methods.messages.Music,
                    methods.messages.Video
                )

            thumb (bool, optional):
                if value is "True",
                    the lib will try to build the thumb ( require cv2 )
                if value is thumbnail.Thumbnail, to set custom
                Defaults to True.
        """
        if object_guid.lower() in ('me', 'cloud', 'self'):
            object_guid = self.guid

        input = {
            'object_guid': object_guid,
            'reply_to_message_id': reply_to_message_id,
            'rnd': int(random() * 1e6 + 1),
        }

        if isinstance(text, str):
            input['text'] = text.strip()

            markdown = self.markdown.to_metadata(text)
            if 'metadata' in markdown.keys():
                input['metadata'] = markdown.get('metadata')
                input['text'] = markdown.get('text')

        if isinstance(sticker, dict):
            input['sticker'] = sticker

        if file_inline:
            if not isinstance(file_inline, Results):
                if isinstance(file_inline, str):
                    if file_inline.startswith('http'):
                        async with aiohttp.ClientSession(headers={'user-agent': self.user_agent}) as cs:
                            async with cs.get(file_inline) as result:
                                if result.ok:
                                    file_name = file_inline.split('/')[-1]
                                    file_inline = await result.read()
                                    kwargs['file_name'] = kwargs.get('file_name',
                                                                     file_name if '.' in file_name else file_name+'.'+type)

                    else:
                        async with aiopen(file_inline, 'rb') as file:
                            kwargs['file_name'] = kwargs.get(
                                'file_name', path.basename(file_inline))
                            file_inline = await file.read()

                if type in ('Music', 'Voice'):
                    thumb = None

                if thumb:
                    if type in ('Video', 'Gif'):
                        thumb = thumbnail.MediaThumbnail.from_video(file_inline)
                    elif type == 'Image':
                        thumb = thumbnail.MediaThumbnail.from_image(file_inline)
                    elif type == 'VideoMessage':
                        thumb = thumbnail.MediaThumbnail.from_video(file_inline)

                    if not hasattr(thumb, 'image'):
                        type = 'File'
                        thumb = None

                file_inline = await self.upload(file_inline, *args, **kwargs)

                if type == 'VideoMessage':
                    file_inline['is_round'] = True

                file_inline['type'] = 'Video' if type == 'VideoMessage' else type
                file_inline['time'] = kwargs.get('time', 1)
                file_inline['width'] = kwargs.get('width', 200)
                file_inline['height'] = kwargs.get('height', 200)
                file_inline['music_performer'] = kwargs.get('performer', '')

                if isinstance(thumb, thumbnail.ResultMedia):
                    file_inline['time'] = thumb.seconds
                    file_inline['width'] = thumb.width
                    file_inline['height'] = thumb.height
                    file_inline['thumb_inline'] = thumb.to_base64()

        if file_inline:
            file_inline['is_spoil'] = bool(is_spoil)
            input['file_inline'] = file_inline.to_dict()

        result = await self.builder('sendMessage', input=input)

        if auto_delete is not None:
            if not isinstance(auto_delete, int):
                raise ValueError('The `auto_delete` parameter can only be Integer.')

            create_task(self.auto_delete_message(result.object_guid,
                                                         result.message_id,
                                                         auto_delete))

        return result
        # message = messages.SendMessage(**result.to_dict())
        # await message.set_shared_data(self, message)
        # return message