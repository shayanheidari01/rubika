import rubpy
from typing import Union
from rubpy.types import Update

class AddChannelMembers:
    async def add_channel_members(
        self: "rubpy.Client",
        channel_guid: str,
        member_guids: Union[str, list],
    ) -> Update:
        """
        Add members to a channel.

        Parameters:
        - channel_guid (str): The unique identifier of the channel.
        - member_guids (Union[str, list]): The unique identifier(s) of the member(s) to be added.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        if isinstance(member_guids, str):
            member_guids = [member_guids]

        return await self.builder(
            'addChannelMembers',
            input={
                'channel_guid': channel_guid,
                'member_guids': member_guids,
            }
        )
