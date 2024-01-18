class GetAvatars:
    async def get_avatars(
            self,
            object_guid: str,
    ):
        return await self.builder('getAvatars',
                                  input={
                                      'object_guid': object_guid,
                                  })