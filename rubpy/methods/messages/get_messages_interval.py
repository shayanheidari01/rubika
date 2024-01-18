from typing import Union


class GetMessagesInterval:
    async def get_messages_interval(
            self,
            object_guid: str,
            middle_message_id: Union[int, str],
    ):
        return await self.builder('getMessagesInterval',
                                  input={
                                      'object_guid': object_guid,
                                      'middle_message_id': str(middle_message_id),
                                  })