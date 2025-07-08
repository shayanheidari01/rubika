import rubpy
from rubpy.types import Update
from typing import Union

class DeleteChatHistory:
    async def delete_chat_history(
            self: "rubpy.Client",
            object_guid: str,
            last_message_id: Union[str, int],
    ) -> Update:
        """
        Delete chat history up to a certain message.

        Parameters:
        - object_guid (str): The unique identifier of the object (e.g., user, chat) for which chat history will be deleted.
        - last_message_id (Union[str, int]): The identifier of the last message to keep in the chat history.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        return await self.builder('deleteChatHistory',
                                  input={
                                      'object_guid': object_guid,
                                      'last_message_id': str(last_message_id),
                                  })
