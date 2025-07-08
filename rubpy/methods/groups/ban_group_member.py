import rubpy
from typing import Optional

class BanGroupMember:
    async def ban_group_member(
            self: "rubpy.Client",
            group_guid: str,
            member_guid: str,
            action: Optional[str] = 'Set',
    ) -> rubpy.types.Update:
        """
        Ban or unban a member from a group.

        Args:
        - group_guid (str): The GUID of the group.
        - member_guid (str): The GUID of the member to be banned or unbanned.
        - action (str): The action to perform. Should be either 'Set' (ban) or 'Unset' (unban).
        
        Returns:
        - rubpy.types.Update: The result of the API call.
        
        Raises:
        - ValueError: If the `action` argument is not 'Set' or 'Unset'.
        """
        if action not in ["Set", "Unset"]:
            raise ValueError('`action` argument can only be in `["Set", "Unset"]`.')

        return await self.builder('banGroupMember',
                                  input={
                                      'group_guid': group_guid,
                                      'member_guid': member_guid,
                                      'action': action,
                                  })
