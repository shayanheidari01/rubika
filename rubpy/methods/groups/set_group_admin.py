import rubpy
from typing import Union

ALLOWEDS = ["SetAdmin", "BanMember", "ChangeInfo", "PinMessages", "SetJoinLink", "SetMemberAccess", "DeleteGlobalAllMessages"]

class SetGroupAdmin:
    async def set_group_admin(
            self: "rubpy.Client",
            group_guid: str,
            member_guid: str,
            action: str = 'SetAdmin',
            access_list: Union[str, list] = [],
    ) -> rubpy.types.Update:
        """
        Set or unset a member as a group admin.

        Args:
        - group_guid (str): The GUID of the group.
        - member_guid (str): The GUID of the member.
        - action (str): The action to perform, either 'SetAdmin' or 'UnsetAdmin'.
        - access_list (Union[str, list]): List of allowed actions. Default is an empty list.

        Returns:
        - rubpy.types.Update: Update object confirming the change in admin status.
        """
        if action not in ('SetAdmin', 'UnsetAdmin'):
            raise ValueError('`action` argument can only be in `["SetAdmin", "UnsetAdmin"]`.')

        if isinstance(access_list, str):
            access_list = list(access_list)

        return await self.builder('setGroupAdmin',
                                  input={
                                      'group_guid': group_guid,
                                      'member_guid': member_guid,
                                      'action': action,
                                      'access_list': access_list,
                                  })
