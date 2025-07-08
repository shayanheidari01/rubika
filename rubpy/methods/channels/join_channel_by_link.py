import rubpy
from rubpy.types import Update

class JoinChannelByLink:
    async def join_channel_by_link(
            self: "rubpy.Client",
            link: str,
    ) -> Update:
        """
        Join a channel using its invite link.

        Parameters:
        - link (str): The invite link or hash of the channel.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        if '/' in link:
            link = link.split('/')[-1]

        return await self.builder('joinChannelByLink',
                                  input={'hash_link': link})
