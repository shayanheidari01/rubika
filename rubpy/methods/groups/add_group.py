from typing import Union


class AddGroup:
    async def add_group(
            self,
            title: str,
            member_guids: Union[str, list],
    ):
        if isinstance(member_guids, str):
            member_guids = list(member_guids)

        return await self.builder('addGroup',
                                  input={
                                      'title': title,
                                      'member_guids': member_guids,
                                  })