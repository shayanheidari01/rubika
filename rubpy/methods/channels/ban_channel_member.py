import rubpy

class BanChannelMember:
    async def ban_channel_member(
            self: "rubpy.Client",
            channel_guid: str,
            member_guid: str,
            action: str = 'Set',
    ):
        if action not in ["Set", "Unset"]:
            raise ValueError('`action` argument can only be in `["Set", "Unset"]`.')

        return await self.builder('banChannelMember',
                                  input={
                                      'channel_guid': channel_guid,
                                      'member_guid': member_guid,
                                      'action': action,
                                  })