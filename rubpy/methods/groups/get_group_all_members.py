import rubpy

class GetGroupAllMembers:
    async def get_group_all_members(
            self: "rubpy.Client",
            group_guid: str,
            search_text: str = None,
            start_id: str = None,
    ) -> rubpy.types.Update:
        """
        Get all members of a group.

        Args:
        - group_guid (str): The GUID of the group.
        - search_text (str, optional): Search text for filtering members. Defaults to None.
        - start_id (str, optional): The starting ID for pagination. Defaults to None.

        Returns:
        - InChatMembers: Object containing information about the group members.
        """
        return await self.builder('getGroupAllMembers',
                                    input={
                                        'group_guid': group_guid,
                                        'search_text': search_text,
                                        'start_id': start_id,
                                    })
