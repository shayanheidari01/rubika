import rubpy

class SearchGlobalObjects:
    async def search_global_objects(
            self: "rubpy.Client",
            search_text: str,
    ) -> rubpy.types.Update:
        """
        Search for global objects (users, channels, etc.) based on the given search text.

        Args:
            search_text (str): The text to search for.

        Returns:
            rubpy.types.Update: The update containing search results.
        """
        return await self.builder('searchGlobalObjects',
                                  input={
                                      'search_text': search_text,
                                  })
