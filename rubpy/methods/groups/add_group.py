import rubpy
from typing import Union, List, Optional

class AddGroup:
    async def add_group(
            self: "rubpy.Client",
            title: str,
            member_guids: Union[str, List[str]],
            description: Optional[str] = None,
    ) -> rubpy.types.Update:
        """
        Add a new group.

        Args:
        - title (str): The title of the group.
        - member_guids (Union[str, List[str]]): A single member GUID or a list of member GUIDs to be added to the group.
        - description (Optional[str]): Description of the group (optional).

        Returns:
        - rubpy.types.Update: The result of the API call.
        """
        if isinstance(member_guids, str):
            member_guids = [member_guids]

        input_data = {
            'title': title,
            'member_guids': member_guids,
            'description': description,
        }

        return await self.builder('addGroup', input=input_data)
