import rubpy
from rubpy.types import Update

class BanChannelMember:
    async def ban_channel_member(
        self: "rubpy.Client",
        channel_guid: str,
        member_guid: str,
        action: str = 'Set',
    ) -> Update:
        """
        Ban or unban a member in a channel.

        Parameters:
        - channel_guid (str): The unique identifier of the channel.
        - member_guid (str): The unique identifier of the member to be banned or unbanned.
        - action (str, optional): The action to perform, can be 'Set' (ban) or 'Unset' (unban). Defaults to 'Set'.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        if action not in ["Set", "Unset"]:
            raise ValueError('`action` argument can only be in `["Set", "Unset"]`.')

        return await self.builder(
            'banChannelMember',
            input={
                'channel_guid': channel_guid,
                'member_guid': member_guid,
                'action': action,
            }
        )
