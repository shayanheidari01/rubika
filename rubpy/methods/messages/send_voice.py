import rubpy

from typing import Union, Optional
from pathlib import Path

class SendVoice:
    async def send_voice(
            self: "rubpy.Client",
            object_guid: str,
            voice: Union[Path, bytes],
            caption: Optional[str] = None,
            reply_to_message_id: Optional[str] = None,
            auto_delete: Optional[int] = None, *args, **kwargs,
    ) -> "rubpy.types.Update":
        """
        Send a voice.

        Args:
            object_guid (str):
                The GUID of the recipient.

            voice (Union[Path, bytes]):
                The voice data.

            caption (str, optional):
                The caption for the voice. Defaults to None.

            reply_to_message_id (str, optional):
                The ID of the message to which this is a reply. Defaults to None.
        """

        # Add a file type check for voice messages
        # if isinstance(voice, Path):
        #     file_extension = voice.suffix.lower()
        #     if file_extension not in ['.ogg', '.opus']:
        #         raise ValueError(f"Unsupported file type for voice messages: {file_extension}")

        return await self.send_message(object_guid=object_guid, text=caption, reply_to_message_id=reply_to_message_id, file_inline=voice, type='Voice', auto_delete=auto_delete, *args, **kwargs)
