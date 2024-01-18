import rubpy

class GetChannelAdminAccessList:
    async def get_channel_admin_access_list(
            self: "rubpy.Client",
            channel_guid: str,
            member_guid: str,
    ):
        return await self.builder('getChannelAdminAccessList',
                                  input={
                                      'channel_guid': channel_guid,
                                      'member_guid': member_guid,
                                  })