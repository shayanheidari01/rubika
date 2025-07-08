import rubpy

class UpdateChannelUsername:
    async def update_channel_username(
            self: "rubpy.Client",
            channel_guid: str,
            username: str,
    ):
        input = {
            'channel_guid': channel_guid,
            'username': username.replace('@', '')
        }

        return await self.builder(
            name='updateChannelUsername',
            input=input,
        )