import rubpy

class GetChannelLink:
    async def get_channel_link(
            self: "rubpy.Client",
            channel_guid: str,
    ):
        return await self.builder('getChannelLink',
                                  input={
                                      'channel_guid': channel_guid,
                                  })