from typing import Union, Optional
from pathlib import Path
import rubpy

class SendVideo:
    async def send_video(
            self: "rubpy.Client",
            object_guid: str,
            video: Union[Path, bytes],
            caption: Optional[str] = None,
            reply_to_message_id: Optional[str] = None,
            is_spoil: bool = False,
            auto_delete: Optional[int] = None, *args, **kwargs,
    ):
        """
        Send a video.

        Args:
            object_guid (str):
                The GUID of the recipient.

            video (Path, bytes):
                The photo data.

            caption (str, optional):
                The caption for the video. Defaults to None.

            reply_to_message_id (str, optional):
                The ID of the message to which this is a reply. Defaults to None.
        """

        return await self.send_message(
            object_guid=object_guid,
            text=caption,
            reply_to_message_id=reply_to_message_id,
            file_inline=video,
            type='Video',
            is_spoil=is_spoil,
            auto_delete=auto_delete, *args, **kwargs)