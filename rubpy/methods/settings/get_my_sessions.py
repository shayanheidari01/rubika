import rubpy

class GetMySessions:
    async def get_my_sessions(self: "rubpy.Client"):
        return await self.builder('getMySessions')