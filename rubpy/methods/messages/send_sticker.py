import rubpy

class SendSticker:
    async def send_sticker(
            self: "rubpy.Client",
            object_guid: str,
            emoji_character: str,
            sticker_id: str,
            sticker_set_id: str,
            file: dict,
            w_h_ratio: str = '1.0',
            reply_to_message_id: str = None,
            auto_delete: int = None,
    ) -> "rubpy.types.Update":
        """
        Send a sticker.

        Args:
            - object_guid (str):
                The GUID of the recipient.

            - emoji_character (str):
                The emoji character associated with the sticker.

            - sticker_id (str):
                The ID of the sticker.

            - sticker_set_id (str):
                The ID of the sticker set.

            - file (dict):
                The file data for the sticker.

            - w_h_ratio (str, optional):
                The width-to-height ratio of the sticker. Defaults to '1.0'.

            - reply_to_message_id (str, optional):
                The ID of the message to which this is a reply. Defaults to None.

            - auto_delete (int, optional):
                Auto-delete duration in seconds. Defaults to None.
        """

        if not isinstance(file, dict):
            file = file.to_dict

        data = {
            'emoji_character': emoji_character,
            'sticker_id': sticker_id,
            'sticker_set_id': sticker_set_id,
            'w_h_ratio': w_h_ratio,
            'file': file,
        }

        return await self.send_message(
            object_guid=object_guid,
            sticker=data,
            reply_to_message_id=reply_to_message_id,
            auto_delete=auto_delete,
        )
