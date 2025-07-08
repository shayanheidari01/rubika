import rubpy
from typing import Union
from rubpy.types import Update

class AddChannel:
    async def add_channel(
        self: "rubpy.Client",
        title: str,
        description: str = None,
        member_guids: Union[str, list] = None,
    ) -> Update:
        """
        Create a new channel and add members if specified.

        Parameters:
        - title (str): The title of the new channel.
        - description (str, optional): The description of the new channel.
        - member_guids (Union[str, list], optional): The unique identifier(s) of the member(s) to be added to the new channel.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        input_data = {'description': description, 'title': title}

        if member_guids is not None:
            if isinstance(member_guids, str):
                member_guids = [member_guids]
            input_data['member_guids'] = member_guids

        return await self.builder('addChannel', input=input_data)
