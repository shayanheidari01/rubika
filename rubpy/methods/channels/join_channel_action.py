import rubpy
from typing import Literal
from rubpy.types import Update

class JoinChannelAction:
    async def join_channel_action(
            self: "rubpy.Client",
            channel_guid: str,
            action: Literal['Join', 'Remove', 'Archive'],
    ) -> Update:
        """
        Perform an action on a channel, such as joining, removing, or archiving.

        Parameters:
        - channel_guid (str): The GUID of the channel.
        - action (Literal['Join', 'Remove', 'Archive']): The action to perform on the channel.

        Returns:
        rubpy.types.Update: The result of the API call.
        """
        if action not in ['Join', 'Remove', 'Archive']:
            raise ValueError('The `action` argument can only be in `["Join", "Remove", "Archive"]`.')

        return await self.builder(
            name='joinChannelAction',
            input=dict(
                channel_guid=channel_guid,
                action=action,
            ))
