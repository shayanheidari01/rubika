import rubpy

from typing import Literal

class ActionOnMessageReaction:
    async def action_on_message_reaction(
            self: "rubpy.Client",
            object_guid: str,
            message_id: str,
            reaction_id: int = None,
            action=Literal['Add', 'Remove'],
    ):
        input = dict(
            object_guid=object_guid,
            message_id=message_id,
            action=action,
            reaction_id=reaction_id,
        )

        return await self.builder(name='actionOnMessageReaction',
                                  input=input)