import rubpy
from ...types.in_chat_members import InChatMembers


class GetMembers:
    async def get_members(
            self: "rubpy.Client",
            object_guid: str,
            start_id: int = None,
            search_text: str = '',
    ) -> InChatMembers:
        if object_guid.startswith('c0'):
            return await self.get_channel_all_members(
                channel_guid=object_guid,
                search_text=search_text,
                start_id=start_id,
            )

        else:
            return await self.get_group_all_members(
                group_guid=object_guid,
                search_text=None if search_text == '' else search_text,
                start_id=start_id,
            )