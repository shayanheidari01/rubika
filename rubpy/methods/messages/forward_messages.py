from typing import Union
from random import random
import rubpy

class ForwardMessages:
    """
    Provides a method to forward messages from one object to another.

    Methods:
    - forward_messages: Forward specified messages from one object to another.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def forward_messages(
            self: "rubpy.Client",
            from_object_guid: str,
            to_object_guid: str,
            message_ids: Union[str, int, list],
    ) -> rubpy.types.Update:
        """
        Forward specified messages from one object to another.

        Parameters:
        - from_object_guid (str): The GUID of the source object from which messages are forwarded.
        - to_object_guid (str): The GUID of the destination object to which messages are forwarded.
        - message_ids (Union[str, int, list]): The IDs of the messages to be forwarded. Can be a single ID or a list of IDs.

        Returns:
        - rubpy.types.Update: The updated information after forwarding the messages.
        """
        if not isinstance(message_ids, list):
            message_ids = [str(message_ids)]

        return await self.builder('forwardMessages',
                                  input={
                                      'from_object_guid': from_object_guid,
                                      'to_object_guid': to_object_guid,
                                      'message_ids': message_ids,
                                      'rnd': int(random() * 1e6 + 1),
                                  })
