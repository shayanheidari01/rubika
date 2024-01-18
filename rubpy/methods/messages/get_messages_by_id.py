from typing import Union


class GetMessagesByID:
    async def get_messages_by_id(
            self,
            object_guid: str,
            message_ids: Union[str, list],
    ):
        if isinstance(message_ids, str):
            message_ids = [str(message_ids)]

        return await self.builder('getMessagesByID',
                                  input={
                                      'object_guid': object_guid,
                                      'message_ids': message_ids,
                                  })