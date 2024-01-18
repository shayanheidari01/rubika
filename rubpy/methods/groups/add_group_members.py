from typing import Union


class AddGroupMembers:
    async def add_group_members(
            self,
            group_guid: str,
            member_guids: Union[str, list],
    ):
        if isinstance(member_guids, str):
            member_guids = [member_guids]

        return await self.builder('addGroupMembers',
                                  input={
                                      'group_guid': group_guid,
                                      'member_guids': member_guids,
                                  })