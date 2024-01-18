from typing import Union


class DeleteMessages:
    async def delete_messages(
            self,
            object_guid: str,
            message_ids: Union[str, list],
            type: str = 'Global',
    ):
        if type not in ('Global', 'Local'):
            raise ValueError('`type` argument can only be in ("Global", "Local").')

        if isinstance(message_ids, str):
            message_ids = [message_ids]

        return await self.builder('deleteMessages',
                                  input={
                                      'object_guid': object_guid,
                                      'message_ids': message_ids,
                                      'type': type,
                                  })