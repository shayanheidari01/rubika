import rubpy

class SearchStickers:
    async def search_stickers(
            self: "rubpy.Client",
            search_text: str = '',
            start_id: str = None,
    ):
        return await self.builder('searchStickers',
                                  input={
                                      'search_text': search_text,
                                      'start_id': str(start_id),
                                  })