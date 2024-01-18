import rubpy

class GetSuggestedFolders:
    async def get_suggested_folders(self: "rubpy.Client"):
        return await self.builder('getSuggestedFolders')