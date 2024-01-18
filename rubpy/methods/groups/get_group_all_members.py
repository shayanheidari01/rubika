import rubpy
from ...types.in_chat_members import InChatMembers


class GetGroupAllMembers:
    async def get_group_all_members(
            self: "rubpy.Client",
            group_guid: str,
            search_text: str = None,
            start_id: str = None,
    ):
        result = await self.builder('getGroupAllMembers',
                                  input={
                                      'group_guid': group_guid,
                                      'search_text': search_text,
                                      'start_id': start_id,
                                  }, dict=True)
        return InChatMembers(**result)