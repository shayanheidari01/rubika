import rubpy
from typing import Union


class DeleteUserChat:
    """
    Provides a method to delete a user chat.

    Methods:
    - delete_user_chat: Delete a user chat.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def delete_user_chat(
            self: "rubpy.Client",
            user_guid: str,
            last_deleted_message_id: Union[str, int],
    ) -> "rubpy.types.Update":
        """
        Delete a user chat.

        Args:
        - user_guid (str): The GUID of the user whose chat is to be deleted.
        - last_deleted_message_id (Union[str, int]): The last deleted message ID.

        Returns:
        - The result of the user chat deletion.
        """
        return await self.builder('deleteUserChat',
                                  input={
                                      'user_guid': user_guid,
                                      'last_deleted_message_id': last_deleted_message_id,
                                  })
