import rubpy
from typing import Union

class DeleteMessages:
    """
    Provides a method to delete messages.

    Methods:
    - delete_messages: Delete specified messages associated with the given object.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def delete_messages(
            self: "rubpy.Client",
            object_guid: str,
            message_ids: Union[str, list],
            type: str = 'Global',
    ) -> rubpy.types.Update:
        """
        Delete specified messages associated with the given object.

        Parameters:
        - object_guid (str): The GUID of the object associated with the messages (e.g., user, group, channel).
        - message_ids (Union[str, list]): The ID or list of IDs of the messages to be deleted.
        - type (str): The type of deletion, can be 'Global' or 'Local'.

        Returns:
        - rubpy.types.Update: The updated information after deleting the messages.
        """
        if type not in ('Global', 'Local'):
            raise ValueError('`type` argument can only be in ("Global", "Local").')

        if isinstance(message_ids, str):
            message_ids = [message_ids]

        return await self.builder('deleteMessages',
                                  input={
                                      'object_guid': object_guid,
                                      'message_ids': message_ids,
                                      'type': type,
                                  })
