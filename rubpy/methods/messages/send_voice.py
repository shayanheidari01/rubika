from typing import Union, Optional
from pathlib import Path
import rubpy

class SendVoice:
    async def send_voice(
            self: "rubpy.Client",
            object_guid: str,
            voice: Union[Path, bytes],
            caption: Optional[str] = None,
            reply_to_message_id: Optional[str] = None,
            auto_delete: Optional[int] = None, *args, **kwargs,
    ):
        """
        Send a voice.

        Args:
            object_guid (str):
                The GUID of the recipient.

            voice (Path, bytes):
                The voice data.

            caption (str, optional):
                The caption for the voice. Defaults to None.

            reply_to_message_id (str, optional):
                The ID of the message to which this is a reply. Defaults to None.
        """

        return await self.send_message(object_guid=object_guid, text=caption, reply_to_message_id=reply_to_message_id, file_inline=voice, type='Voice', auto_delete=auto_delete, *args, **kwargs)