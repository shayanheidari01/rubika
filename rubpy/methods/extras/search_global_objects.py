class SearchGlobalObjects:
    async def search_global_objects(
            self,
            search_text: str,
    ):
        return await self.builder('searchGlobalObjects',
                                  input={
                                      'search_text': search_text,
                                  })