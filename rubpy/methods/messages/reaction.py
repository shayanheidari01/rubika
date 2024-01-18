import rubpy

class Reaction:
    async def reaction(
            self: "rubpy.Client",
            object_guid: str,
            message_id: str,
            reaction_id: int,
    ):
        return await self.action_on_message_reaction(
            object_guid=object_guid,
            message_id=message_id,
            action='Add',
            reaction_id=reaction_id,
        )