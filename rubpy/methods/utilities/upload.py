import rubpy


class UploadFile:
    async def upload(self: "rubpy.Client", file, *args, **kwargs):
        return await self.connection.upload_file(file=file, *args, **kwargs)