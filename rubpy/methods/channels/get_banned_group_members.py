from typing import Optional
import rubpy
from rubpy.types import Update

class GetBannedGroupMembers:
    async def get_banned_group_members(
            self: "rubpy.Client",
            group_guid: str,
            start_id: Optional[str] = None,
    ) -> Update:
        """
        Get a list of banned members in a group.

        Parameters:
        - group_guid (str): The GUID of the group.
        - start_id (str, optional): The ID to start retrieving banned members from.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        return await self.builder('getBannedGroupMembers', input={'group_guid': group_guid, 'start_id': start_id})
