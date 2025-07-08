import rubpy
from rubpy.types import Update

class GetChannelAllMembers:
    async def get_channel_all_members(
            self: "rubpy.Client",
            channel_guid: str,
            search_text: str=None,
            start_id: str=None,
    ) -> Update:
        """
        Get all members in a channel.

        Parameters:
        - channel_guid (str): The GUID of the channel.
        - search_text (str, optional): Text to search for in members. Defaults to None.
        - start_id (str, optional): The ID to start fetching from. Defaults to None.

        Returns:
        rubpy.types.InChatMembers: The result of the API call.
        """
        return await self.builder('getChannelAllMembers', input={'channel_guid': channel_guid, 'search_text': search_text, 'start_id': start_id})