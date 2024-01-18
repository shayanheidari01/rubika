from typing import Union


class DeleteChatHistory:
    async def delete_chat_history(
            self,
            object_guid: str,
            last_message_id: Union[str, int],
    ):
        return await self.builder('deleteChatHistory',
                                  input={
                                      'object_guid': object_guid,
                                      'last_message_id': str(last_message_id),
                                  })