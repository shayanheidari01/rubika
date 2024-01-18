import rubpy

class DeleteFolder:
    async def delete_folder(
            self: "rubpy.Client",
            folder_id: str,
    ):
        return await self.builder(name='deleteFolder',
                                  input={'folder_id': str(folder_id)})