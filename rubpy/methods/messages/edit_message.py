from typing import Union
import rubpy

class EditMessage:
    async def edit_message(
            self: "rubpy.Client",
            object_guid: str,
            message_id: Union[int, str],
            text: str,
            parse_mode: str = None,
    ):
        parse_mode = parse_mode or self.parse_mode
        input = {
            'object_guid': object_guid,
            'message_id': str(message_id),
            'text': text.strip(),
            }

        if isinstance(parse_mode, str):
            if parse_mode == 'html':
                markdown = self.markdown.to_metadata(self.markdown.to_markdown(text))

            else:
                markdown = self.markdown.to_metadata(text)

            if 'metadata' in markdown.keys():
                input['metadata'] = markdown.get('metadata')
                input['text'] = markdown.get('text')

        return await self.builder(name='editMessage',
                                  input=input)