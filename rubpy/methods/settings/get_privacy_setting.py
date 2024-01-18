import rubpy

class GetPrivacySetting:
    async def get_privacy_setting(self: "rubpy.Client"):
        return await self.builder('getPrivacySetting')