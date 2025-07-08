from ...types import Update
from ...enums import ParseMode
from ..utilities import thumbnail
from typing import Optional, Union
from asyncio import create_task
from pathlib import Path
from os import path
from random import random
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
        auto_delete: Optional[Union[int, float]] = None,
        parse_mode: Optional[Union[ParseMode, str]] = None,
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
                async with aiofiles.open(file_inline, 'rb+') as file:
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

            # Finalize input for sending the message
            file_inline['is_spoil'] = bool(is_spoil)

        if file_inline is not None:
            input['file_inline'] = file_inline if isinstance(file_inline, dict) else file_inline.to_dict

        # Send the message
        result = await self.builder('sendMessage', input=input)

        # Schedule auto-delete if specified
        if isinstance(auto_delete, (int, float)):
            create_task(self.auto_delete_message(
                result.object_guid, result.message_id, auto_delete))

        return result
