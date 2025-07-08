import rubpy

class SetActionChat:
    async def set_action_chat(
            self: "rubpy.Client",
            object_guid: str,
            action: str='Mute',
    ) -> rubpy.types.Update:
        """
        Set the action for a chat, such as muting or unmuting.

        Args:
            object_guid (str): The GUID of the chat.
            action (str, optional): The action to be set. Defaults to 'Mute'.

        Returns:
            rubpy.types.Update: The result of the operation.

        Raises:
            ValueError: If the `action` argument is not one of `["Mute", "Unmute"]`.
        """
        if action not in ('Mute', 'Unmute'):
            raise ValueError('`action` argument can only be `Mute` or `Unmute`.')

        return await self.builder('setActionChat',
                                  input={
                                      'object_guid': object_guid,
                                      'action': action,
                                  })
