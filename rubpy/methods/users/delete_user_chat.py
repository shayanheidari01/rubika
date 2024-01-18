from typing import Union


class DeleteUserChat:
    async def delete_user_chat(
            self,
            user_guid: str,
            last_deleted_message_id: Union[str, int],
    ):
        return await self.builder('deleteUserChat',
                                  input={
                                      'user_guid': user_guid,
                                      'last_deleted_message_id': last_deleted_message_id,
                                  })