class CheckUserUsername:
    async def check_user_username(self, username: str):
        return await self.builder('checkUserUsername',
                                  input={'username': username})