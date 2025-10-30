from typing import Optional
import rubpy


class GetMessageReactions:
    async def get_message_reactions(
        self: "rubpy.Client",
        object_guid: str,
        message_id: str,
        start_id: Optional[str] = None,
    ):
        return await self.builder(
            name="getMessageReactions",
            input={
                "object_guid": object_guid,
                "message_id": message_id,
                "start_id": start_id,
            },
        )
