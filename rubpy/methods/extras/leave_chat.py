import rubpy

class LeaveChat:
    async def leave_chat(
            self: "rubpy.Client",
            object_guid: str,
    ) -> rubpy.types.Update:
        """
        Leave a chat (channel or group).

        Args:
            object_guid (str): The identifier of the chat (channel or group).

        Returns:
            rubpy.types.Update: The update containing information about leaving the chat.
        """
        if object_guid.startswith('c0'):
            return await self.join_channel_action(object_guid, 'Remove')
        elif object_guid.startswith('g0'):
            return await self.leave_group(object_guid)
