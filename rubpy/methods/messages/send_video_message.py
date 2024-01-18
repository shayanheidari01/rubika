import rubpy

from typing import Optional, Union
from pathlib import Path

class SendVideoMessage:
    async def send_video_message(
            self: "rubpy.Client",
            object_guid: str,
            video_message: Union[Path, bytes],
            caption: Optional[str] = None,
            reply_to_message_id: Optional[str] = None,
            auto_delete: Optional[int] = None, *args, **kwargs,
    ):
        """
        Send a video message.

        Args:
            object_guid (str):
                The GUID of the recipient.

            video_message (Path, bytes):
                The photo data.

            caption (str, optional):
                The caption for the video. Defaults to None.

            reply_to_message_id (str, optional):
                The ID of the message to which this is a reply. Defaults to None.
        """

        return await self.send_message(object_guid=object_guid, text=caption, reply_to_message_id=reply_to_message_id, file_inline=video_message, type='VideoMessage', auto_delete=auto_delete, *args, **kwargs)