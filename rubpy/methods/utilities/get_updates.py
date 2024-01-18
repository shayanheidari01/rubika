import rubpy


class GetUpdates:
    async def get_updates(self: "rubpy.Client"):
        return await self.connection.get_updates()