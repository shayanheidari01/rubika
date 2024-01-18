import rubpy

class GetTwoPasscodeStatus:
    async def get_two_passcode_status(self: "rubpy.Client"):
        return await self.builder('getTwoPasscodeStatus')