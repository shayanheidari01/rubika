from typing import Union


class EditMessage:
    async def edit_message(
            self,
            object_guid: str,
            message_id: Union[int, str],
            text: str,
    ):
        input = {
            'object_guid': object_guid,
            'message_id': str(message_id),
            'text': text.strip(),
            }

        markdown = self.markdown.to_metadata(text)
        if 'metadata' in markdown.keys():
            input['metadata'] = markdown.get('metadata')
            input['text'] = markdown.get('text')

        return await self.builder('editMessage',
                                  input=input)