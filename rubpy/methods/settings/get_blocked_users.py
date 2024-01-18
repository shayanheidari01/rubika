import rubpy

class GetBlockedUsers:
    async def get_blocked_users(self: "rubpy.Client"):
        return await self.builder('getBlockedUsers')