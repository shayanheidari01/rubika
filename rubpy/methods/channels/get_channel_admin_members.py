import rubpy
from rubpy.types import Update

class GetChannelAdminMembers:
    async def get_channel_admin_members(
            self: "rubpy.Client",
            channel_guid: str,
            start_id: str=None,
    ) -> Update:
        """
        Get the list of admin members in a channel.

        Parameters:
        - channel_guid (str): The GUID of the channel.
        - start_id (str, optional): The ID to start fetching from. Defaults to None.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        return await self.builder('getChannelAdminMembers', input={'channel_guid': channel_guid, 'start_id': start_id})
