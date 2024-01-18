class GetObjectByUsername:
    async def get_object_by_username(
            self,
            username: str,
    ):
        username = username.replace('@', '')
        return await self.builder('getObjectByUsername',
                                  input={
                                      'username': username,
                                  })