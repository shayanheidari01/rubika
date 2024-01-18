class SearchChatMessages:
    async def search_chat_messages(
            self,
            object_guid: str,
            search_text: str,
            type: str = 'Text',
    ):
        if type not in ('Text', 'Hashtag'):
            raise ValueError('`type` argument can only be in ("text", "Hashtag").')

        return await self.builder('searchChatMessages',
                                  input={
                                      'object_guid': object_guid,
                                      'search_text': search_text,
                                      'type': type,
                                  })