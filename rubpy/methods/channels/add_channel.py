import rubpy
from typing import Union


class AddChannel:
    async def add_channel(
            self: "rubpy.Client",
            title: str,
            description: str = None,
            member_guids: Union[str, list] = None,
    ):
        input = {'description': description,
                 'title': title}

        if member_guids is not None:
            if isinstance(member_guids, str):
                member_guids = [member_guids]
            input['member_guids'] = member_guids

        return await self.builder('addChannel',
                                  input=input)