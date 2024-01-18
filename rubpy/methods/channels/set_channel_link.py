import rubpy

class SetChannelLink:
    async def set_channel_link(
            self: "rubpy.Client",
            channel_guid: str,
    ):
        return await self.builder('setChannelLink',
                                  input={
                                      'channel_guid': channel_guid,
                                  })