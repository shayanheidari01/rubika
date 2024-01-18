import rubpy
from typing import Literal


class JoinChannelAction:
    async def join_channel_action(
            self: "rubpy.Client",
            channel_guid: str,
            action: Literal['Join', 'Remove', 'Archive'],
    ):
        if action not in ['Join', 'Remove', 'Archive']:
            raise ValueError('The `action` argument can only be in `["Join", "Remove", "Archive"]`.')

        return await self.builder(
            name='joinChannelAction',
            input=dict(
                channel_guid=channel_guid,
                action=action,
                ))