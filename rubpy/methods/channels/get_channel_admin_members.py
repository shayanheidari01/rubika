import rubpy

class GetChannelAdminMembers:
    async def get_channel_admin_members(
            self,
            channel_guid: str,
            start_id: str=None,
    ):
        return await self.builder('getChannelAdminMembers',
                                  input={
                                      'channel_guid': channel_guid,
                                      'start_id': start_id,
                                  })