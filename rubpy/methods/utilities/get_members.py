import rubpy

class GetMembers:
    async def get_members(
            self: "rubpy.Client",
            object_guid: str,
            start_id: int = None,
            search_text: str = '',
    ) -> "rubpy.types.Update":
        """
        Get members of a group or channel.

        Args:
        - object_guid (str): The GUID of the group or channel.
        - start_id (int, optional): The starting ID for fetching members.
        - search_text (str, optional): The text to search for among members.

        Returns:
        - rubpy.types.Update: An Update object containing information about the members.

        Raises:
        - ValueError: If the object_guid does not start with 'c0' or 'g0'.
        """

        if object_guid.startswith('c0'):
            # Get members for a channel
            return await self.get_channel_all_members(
                channel_guid=object_guid,
                search_text=search_text,
                start_id=start_id,
            )
        elif object_guid.startswith('g0'):
            # Get members for a group
            return await self.get_group_all_members(
                group_guid=object_guid,
                search_text=None if search_text == '' else search_text,
                start_id=start_id,
            )
        else:
            raise ValueError("Invalid object_guid. Must start with 'c0' or 'g0'.")
