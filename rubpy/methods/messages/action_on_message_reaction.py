import rubpy
from typing import Literal

class ActionOnMessageReaction:
    """
    Provides a method to perform actions on reactions to a specific message.

    Methods:
    - action_on_message_reaction: Perform actions on reactions to a specific message.

    Attributes:
    - self (rubpy.Client): The rubpy client instance.
    """

    async def action_on_message_reaction(
            self: "rubpy.Client",
            object_guid: str,
            message_id: str,
            reaction_id: int = None,
            action: Literal['Add', 'Remove'] = 'Add',
    ) -> rubpy.types.Update:
        """
        Perform actions on reactions to a specific message.

        Parameters:
        - object_guid (str): The GUID of the object associated with the message (e.g., user, group, channel).
        - message_id (str): The ID of the message.
        - reaction_id (int): The ID of the reaction.
        - action (Literal['Add', 'Remove']): The action to perform on the reaction.

        Returns:
        - rubpy.types.Update: The updated information after performing the action on the message reaction.
        """
        input_params = {
            'object_guid': object_guid,
            'message_id': message_id,
            'action': action,
            'reaction_id': reaction_id,
        }

        return await self.builder(name='actionOnMessageReaction', input=input_params)
