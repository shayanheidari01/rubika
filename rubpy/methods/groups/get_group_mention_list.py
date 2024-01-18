class GetGroupMentionList:
    async def get_group_mention_list(
            self,
            group_guid: str,
            search_mention: str = None,
    ):
        return await self.builder('getGroupMentionList',
                                  input={
                                      'group_guid': group_guid,
                                      'search_mention': search_mention,
                                  })