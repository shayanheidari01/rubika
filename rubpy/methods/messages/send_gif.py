from typing import Union, Optional
from pathlib import Path
import rubpy

class SendGif:
    async def send_gif(
            self: "rubpy.Client",
            object_guid: str,
            gif: Union[Path, bytes],
            caption: Optional[str] = None,
            reply_to_message_id: Optional[str] = None,
            auto_delete: Optional[int] = None, *args, **kwargs,
    ):
        """
        Send a gif.

        Args:
            object_guid (str):
                The GUID of the recipient.

            gif (Path, bytes):
                The gif data.

            caption (str, optional):
                The caption for the gif. Defaults to None.

            reply_to_message_id (str, optional):
                The ID of the message to which this is a reply. Defaults to None.
        """

        return await self.send_message(object_guid=object_guid, text=caption, reply_to_message_id=reply_to_message_id, file_inline=gif, type='Gif', auto_delete=auto_delete, *args, **kwargs)