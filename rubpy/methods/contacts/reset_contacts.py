import rubpy

class ResetContacts:
    async def reset_contacts(self: "rubpy.Client"):
        return await self.builder("resetContacts")