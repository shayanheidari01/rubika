import rubpy

class SearchChatMessages:
    async def search_chat_messages(
            self: "rubpy.Client",
            object_guid: str,
            search_text: str,
            type: str = 'Text',
    ) -> rubpy.types.Update:
        """
        Searches for chat messages based on the specified criteria.

        Args:
            object_guid (str): The GUID of the chat or channel.
            search_text (str): The text to search for in messages.
            type (str, optional): The type of search, can be 'Text' or 'Hashtag'. Defaults to 'Text'.

        Returns:
            rubpy.types.Update: The search results.

        Raises:
            ValueError: If the `type` argument is not valid.
            rubpy.exceptions.APIError: If the API request fails.
        """
        if type not in ('Text', 'Hashtag'):
            raise ValueError('`type` argument can only be in ("text", "Hashtag").')

        return await self.builder('searchChatMessages',
                                  input={
                                      'object_guid': object_guid,
                                      'search_text': search_text,
                                      'type': type,
                                  })
