from typing import Union
import rubpy

class AddChannelMembers:
    async def add_channel_members(
            self: "rubpy.Client",
            channel_guid: str,
            member_guids: Union[str, list],
    ):
        if isinstance(member_guids, str):
            member_guids = [member_guids]

        return await self.builder('addChannelMembers',
                                  input={
                                      'channel_guid': channel_guid,
                                      'member_guids': member_guids,
                                  })