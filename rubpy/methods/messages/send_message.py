from ..utilities import thumbnail, audio
from ...types import Update

from typing import Optional, Union
from asyncio import create_task
from random import random
from pathlib import Path
from os import path

import rubpy
import aiohttp
import aiofiles
import mimetypes


async def get_mime_from_url(session: "aiohttp.ClientSession", url: str):
    async with session.head(url) as response:
        content_type = response.content_type
        if content_type:
            return mimetypes.guess_extension(content_type.split(';')[0])


class SendMessage:
    """
    Class to send messages with attachments.

    Methods:
    - send_message: Send a message with various optional parameters.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def send_message(
        self: "rubpy.Client",
        object_guid: str,
        text: Optional[str] = None,
        reply_to_message_id: Optional[str] = None,
        file_inline: Optional[Union[Update, Path, bytes]] = None,
        sticker: Optional[Union[Update, dict]] = None,
        type: str = 'File',
        is_spoil: bool = False,
        thumb: bool = True,
        audio_info: bool = True,
        auto_delete: Optional[Union[int, float]] = None,
        parse_mode: Optional[Union['rubpy.enums.ParseMode', str]] = None,
        metadata: Optional[Union[Update, dict]] = None,
        *args, **kwargs,
    ) -> rubpy.types.Update:
        """
        Send a message with optional parameters.

        Parameters:
        - object_guid (str): The GUID of the recipient.
        - text (Optional[str]): The text of the message. Defaults to None.
        - reply_to_message_id (Optional[str]): The ID of the message to which this is a reply. Defaults to None.
        - file_inline (Optional[Union[Update, Path, bytes]]): The file to be sent inline with the message. Defaults to None.
        - sticker (Optional[Union[Update, dict]]): The sticker to be sent with the message. Defaults to None.
        - type (str): The type of the message, e.g., 'File', 'Music', 'Voice', etc. Defaults to 'File'.
        - is_spoil (bool): Whether the message should be marked as a spoiler. Defaults to False.
        - thumb (bool): Whether to include a thumbnail. Defaults to True.
        - auto_delete (Optional[Union[int, float]]): Auto-delete duration in seconds. Defaults to None.
        - parse_mode (Optional[Union[ParseMode, str]]): The parse mode for the text. Defaults to None.
        - args, kwargs: Additional arguments and keyword arguments.

        Returns:
        - rubpy.types.Update: The update indicating the success of the message sending.
        """
        if object_guid.lower() in ('me', 'cloud', 'self'):
            object_guid = self.guid

        input = dict(
            object_guid=object_guid,
            reply_to_message_id=reply_to_message_id,
            rnd=int(random() * 1e6 + 1),
        )

        # Process text content and parse mode
        if isinstance(text, str):
            if metadata:
                if 'metadata' in metadata:
                    input.update(metadata)
                else:
                    input['metadata'] = metadata

            input['text'] = text.strip()
            parse_mode = parse_mode or self.parse_mode
            if isinstance(parse_mode, str):
                input.update(
                    self.markdown.to_metadata(
                        self.markdown.to_markdown(text))
                    if parse_mode == 'html' else
                    self.markdown.to_metadata(text)
                )

        # Process sticker content
        if isinstance(sticker, (Update, dict)):
            input['sticker'] = (
                sticker.original_update
                if isinstance(sticker, Update)
                else sticker
            )

        # Process inline file content
        if file_inline is not None and isinstance(file_inline, str):
            if not file_inline.startswith('http'):
                async with aiofiles.open(file_inline, 'rb') as file:
                    kwargs['file_name'] = kwargs.get(
                        'file_name', path.basename(file_inline))
                    file_inline = await file.read()
            else:
                async with aiohttp.ClientSession(headers={'user-agent': self.user_agent}) as cs:
                    mime = await get_mime_from_url(session=cs, url=file_inline)
                    kwargs['file_name'] = kwargs.get(
                        'file_name',
                        ''.join([str(input['rnd']), mime if mime else ''.join(['.', type])])
                    )
                    async with cs.get(file_inline) as result:
                        file_inline = await result.read()

        if isinstance(file_inline, bytes):
            # Process thumbnail
            if type in ('Music', 'Voice'):
                thumb = None
                if audio_info is True:
                    audio_info = audio.Audio.get_audio_info(file_inline)

            if thumb:
                if type in ('Video', 'Gif', 'VideoMessage'):
                    thumb = thumbnail.MediaThumbnail.from_video(file_inline)
                elif type == 'Image':
                    thumb = thumbnail.MediaThumbnail.from_image(file_inline)

            if thumb is not None and not hasattr(thumb, 'image'):
                type = 'File'
                thumb = None

            # Upload the file
            file_inline = await self.upload(file_inline, *args, **kwargs)

            # Additional processing based on file type
            if type == 'VideoMessage':
                file_inline['is_round'] = True

            file_inline['type'] = 'Video' if type == 'VideoMessage' else type
            file_inline['time'] = kwargs.get('time', 1)
            file_inline['width'] = kwargs.get('width', 200)
            file_inline['height'] = kwargs.get('height', 200)
            file_inline['music_performer'] = kwargs.get('performer', '')

            # Process thumbnail for inline display
            if isinstance(thumb, thumbnail.ResultMedia):
                file_inline['time'] = thumb.seconds
                file_inline['width'] = thumb.width
                file_inline['height'] = thumb.height
                file_inline['thumb_inline'] = thumb.to_base64()
            
            if isinstance(audio_info, audio.AudioResult):
                file_inline['music_performer'] = kwargs.get('performer', audio_info.performer)
                file_inline['time'] = kwargs.get('time', audio_info.duration if type == 'Music' else audio_info.duration * 1000)

            # Finalize input for sending the message
            file_inline['is_spoil'] = bool(is_spoil)

        # Send the message
        if file_inline is not None:
            input['file_inline'] = file_inline if isinstance(file_inline, dict) else file_inline.to_dict
            result = await self.builder('sendMessage', input=input)

        else:
            if 'text' in input:
                chunks = [input['text'][i:i+4200] for i in range(0, len(input['text']), 4200)]
                if not chunks:
                    result = await self.builder('sendMessage', input=input)
                else:
                    for chunk in chunks:
                        input['text'] = chunk.strip()
                        result = await self.builder('sendMessage', input=input)

        # Schedule auto-delete if specified
        if isinstance(auto_delete, (int, float)):
            create_task(self.auto_delete_message(
                result.object_guid, result.message_id, auto_delete))

        return result
