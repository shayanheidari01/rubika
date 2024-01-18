from typing import Optional
import rubpy

class EditChannelInfo:
    async def edit_channel_info(
            self: "rubpy.Client",
            channel_guid: str,
            title: Optional[str]=None,
            description: Optional[str]=None,
            channel_type: Optional[str]=None,
            sign_messages: Optional[str]=None,
            chat_reaction_setting: Optional[dict]=None,
            chat_history_for_new_members: Optional[str]=None,
    ):
        updated_parameters = []
        input = {
            'channel_guid': channel_guid,
        }

        if title is not None:
            input['title'] = title
            updated_parameters.append('title')

        if description is not None:
            input['description'] = description
            updated_parameters.append('description')

        if channel_type is not None:
            input['channel_type'] = channel_type
            updated_parameters.append('channel_type')

        if sign_messages is not None:
            input['sign_messages'] = sign_messages
            updated_parameters.append('sign_messages')

        if chat_reaction_setting is not None:
            input['chat_reaction_setting'] = chat_reaction_setting
            updated_parameters.append('chat_reaction_setting')

        if chat_history_for_new_members is not None:
            if chat_history_for_new_members not in ('Hidden', 'Visible'):
                raise ValueError('`chat_history_for_new_members` argument can only be in `["Hidden", "Visible"]`.')

            input['chat_history_for_new_members'] = chat_history_for_new_members
            updated_parameters.append('chat_history_for_new_members')

        input['updated_parameters'] = updated_parameters
        return await self.builder('editChannelInfo',
                                  input=input)