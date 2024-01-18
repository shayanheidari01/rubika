from typing import Union

ALLOWEDS = ["SetAdmin", "BanMember", "ChangeInfo", "PinMessages", "SetJoinLink", "SetMemberAccess", "DeleteGlobalAllMessages"]

class SetGroupAdmin:
    async def set_group_admin(
            self,
            group_guid: str,
            member_guid: str,
            action: str = 'SetAdmin',
            access_list: Union[str, list]=[],
    ):
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