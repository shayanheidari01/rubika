from typing import Union, Literal


class SetPinMessage:
    async def set_pin_message(
            self,
            object_guid: str,
            message_id: Union[str, int],
            action: str = Literal['Pin', 'Unpin']
    ):
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
    ):
        return await self.set_pin_message(object_guid=object_guid,
                                          message_id=message_id, action='Pin')

    async def set_unpin(
            self,
            object_guid: str,
            message_id: Union[str, int],
    ):
        return await self.set_pin_message(object_guid=object_guid,
                                          message_id=message_id, action='Unpin')