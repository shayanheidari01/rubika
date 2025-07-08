import rubpy
from time import time

class GetMessagesUpdates:
    """
    Provides a method to get message updates for a specific object.

    Methods:
    - get_messages_updates: Get message updates for a specific object.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def get_messages_updates(
            self: "rubpy.Client",
            object_guid: str,
            state: int = round(time()) - 150,
    ) -> rubpy.types.Update:
        """
        Get message updates for a specific object.

        Parameters:
        - object_guid (str): The GUID of the object for which updates are requested.
        - state (int): The state at which updates are requested. Defaults to a timestamp approximately 150 seconds ago.

        Returns:
        - rubpy.types.Update: The message updates for the specified object.
        """
        return await self.builder('getMessagesUpdates',
                                  input=dict(
                                      object_guid=object_guid,
                                      state=int(state),
                                  ))
