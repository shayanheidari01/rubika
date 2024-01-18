from typing import Optional


class EditGroupInfo:
    async def edit_group_info(
            self,
            group_guid: str,
            title: Optional[str]=None,
            description: Optional[str]=None,
            slow_mode: Optional[str]=None,
            event_messages: Optional[bool]=None,
            chat_reaction_setting: Optional[dict]=None,
            chat_history_for_new_members: Optional[str]=None,
    ):
        updated_parameters = []
        input = {
            'group_guid': group_guid,
        }

        if title is not None:
            input['title'] = title
            updated_parameters.append('title')

        if description is not None:
            input['description'] = description
            updated_parameters.append('description')

        if slow_mode is not None:
            input['slow_mode'] = slow_mode
            updated_parameters.append('slow_mode')

        if event_messages is not None:
            input['event_messages'] = event_messages
            updated_parameters.append('event_messages')

        if chat_reaction_setting is not None:
            input['chat_reaction_setting'] = chat_reaction_setting
            updated_parameters.append('chat_reaction_setting')

        if chat_history_for_new_members is not None:
            if chat_history_for_new_members not in ('Hidden', 'Visible'):
                raise ValueError('`chat_history_for_new_members` argument can only be in `["Hidden", "Visible"]`.')

            input['chat_history_for_new_members'] = chat_history_for_new_members
            updated_parameters.append('chat_history_for_new_members')

        input['updated_parameters'] = updated_parameters
        return await self.builder('editGroupInfo',
                                  input=input)