from typing import Union, Optional
from pathlib import Path
import rubpy

class SendMusic:
    async def send_music(
            self: "rubpy.Client",
            object_guid: str,
            music: Union[Path, bytes],
            caption: Optional[str] = None,
            reply_to_message_id: Optional[str] = None,
            auto_delete: Optional[int] = None, *args, **kwargs,
    ):
        """
        Send a music.

        Args:
            object_guid (str):
                The GUID of the recipient.

            music (Path, bytes):
                The music data.

            caption (str, optional):
                The caption for the music. Defaults to None.

            reply_to_message_id (str, optional):
                The ID of the message to which this is a reply. Defaults to None.
        """

        return await self.send_message(object_guid=object_guid, text=caption, reply_to_message_id=reply_to_message_id, file_inline=music, type='Music', auto_delete=auto_delete, *args, **kwargs)