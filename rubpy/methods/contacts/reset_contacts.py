import rubpy

class ResetContacts:
    async def reset_contacts(self: "rubpy.Client"):
        return self.builder("resetContacts")