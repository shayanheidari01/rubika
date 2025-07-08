from typing import Union, Literal
import rubpy

class SetPinMessage:
    async def set_pin_message(
            self,
            object_guid: str,
            message_id: Union[str, int],
            action: Literal['Pin', 'Unpin'] = 'Pin',
    ) -> rubpy.types.Update:
        """
        Set or unset a pin on a message.

        Args:
            - object_guid (str): The GUID of the recipient.
            - message_id (Union[str, int]): The ID of the message to pin or unpin.
            - action (Literal['Pin', 'Unpin']): The action to perform, either 'Pin' or 'Unpin'.

        Returns:
            - rubpy.types.Update: The update indicating the success of the operation.
        """
        if action not in ('Pin', 'Unpin'):
            raise ValueError('The `action` argument can only be in `("Pin", "Unpin")`.')

        return await self.builder('setPinMessage',
                                  input={
                                      'object_guid': object_guid,
                                      'message_id': str(message_id),
                                      'action': action,
                                  })

    async def set_pin(
            self,
            object_guid: str,
            message_id: Union[str, int],
    ) -> rubpy.types.Update:
        """
        Set a pin on a message.

        Args:
            - object_guid (str): The GUID of the recipient.
            - message_id (Union[str, int]): The ID of the message to pin.

        Returns:
            - rubpy.types.Update: The update indicating the success of setting the pin.
        """
        return await self.set_pin_message(object_guid=object_guid,
                                          message_id=message_id, action='Pin')

    async def set_unpin(
            self,
            object_guid: str,
            message_id: Union[str, int],
    ) -> rubpy.types.Update:
        """
        Unset a pin on a message.

        Args:
            - object_guid (str): The GUID of the recipient.
            - message_id (Union[str, int]): The ID of the message to unpin.

        Returns:
            - rubpy.types.Update: The update indicating the success of unsetting the pin.
        """
        return await self.set_pin_message(object_guid=object_guid,
                                          message_id=message_id, action='Unpin')
