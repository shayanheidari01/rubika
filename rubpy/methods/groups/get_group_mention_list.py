import rubpy

class GetGroupMentionList:
    async def get_group_mention_list(
            self,
            group_guid: str,
            search_mention: str = None,
    ) -> rubpy.types.Update:
        """
        Get the mention list for a group.

        Args:
        - group_guid (str): The GUID of the group.
        - search_mention (str, optional): Search text for mentions.

        Returns:
        - rubpy.types.Update: Update object containing the group mention list.
        """
        return await self.builder('getGroupMentionList',
                                  input={
                                      'group_guid': group_guid,
                                      'search_mention': search_mention,
                                  })
