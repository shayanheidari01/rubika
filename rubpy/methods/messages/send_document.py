from typing import Optional, Union
from pathlib import Path
import rubpy

class SendDocmuent:
    async def send_document(
                self: "rubpy.Client",
                object_guid: str,
                document: Union[Path, bytes],
                caption: Optional[str] = None,
                reply_to_message_id:Optional[str] = None,
                auto_delete: Optional[int]=None, *args, **kwargs,
    ):
        """
        Send a document.

        Args:
            object_guid (str):
                The GUID of the recipient.

            document (bytes):
                The document data.

            caption (str, optional):
                The caption for the document. Defaults to None.

            reply_to_message_id (str, optional):
                The ID of the message to which this is a reply. Defaults to None.
        """
        return await self.send_message(object_guid=object_guid, text=caption, reply_to_message_id=reply_to_message_id, file_inline=document, thumb=False, auto_delete=auto_delete, *args, **kwargs)