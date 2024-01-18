import rubpy

class UpdateUsername:
    async def update_username(self: "rubpy.Client", username: str):
        return await self.builder('updateUsername', input={'username': username.replace('@', '')})