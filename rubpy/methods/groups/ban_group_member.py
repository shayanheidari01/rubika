class BanGroupMember:
    async def ban_group_member(
            self,
            group_guid: str,
            member_guid: str,
            action: str = 'Set',
    ):
        if action not in ["Set", "Unset"]:
            raise ValueError('`action` argument can only be in `["Set", "Unset"]`.')

        return await self.builder('banGroupMember',
                                  input={
                                      'group_guid': group_guid,
                                      'member_guid': member_guid,
                                      'action': action,
                                  })