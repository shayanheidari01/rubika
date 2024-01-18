class DeleteAvatar:
    async def delete_avatar(
            self,
            object_guid: str,
            avatar_id: str,
    ):
        return await self.builder('deleteAvatar',
                                  input={
                                      'object_guid': object_guid,
                                      'avatar_id': avatar_id,
                                  })