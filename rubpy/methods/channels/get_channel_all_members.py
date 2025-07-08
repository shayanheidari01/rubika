import rubpy
from ...types.in_chat_members import InChatMembers


class GetChannelAllMembers:
    async def get_channel_all_members(
            self: "rubpy.Client",
            channel_guid: str,
            search_text: str=None,
            start_id: str=None,
    ):
        result = await self.builder('getChannelAllMembers',
                                  input={
                                      'channel_guid': channel_guid,
                                      'search_text': search_text,
                                      'start_id': start_id,
                                  }, dict=True)
        return InChatMembers(**result)