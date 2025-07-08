from typing import Optional, Union, Dict
import rubpy

class EditGroupInfo:
    async def edit_group_info(
            self: "rubpy.Client",
            group_guid: str,
            title: Optional[str] = None,
            description: Optional[str] = None,
            slow_mode: Optional[str] = None,
            event_messages: Optional[bool] = None,
            chat_reaction_setting: Optional[Dict[str, Union[str, int]]] = None,
            chat_history_for_new_members: Optional[str] = None,
    ) -> rubpy.types.Update:
        """
        Edit the information of a group.

        Args:
        - group_guid (str): The GUID of the group.
        - title (Optional[str]): The new title for the group.
        - description (Optional[str]): The new description for the group.
        - slow_mode (Optional[str]): The new slow mode setting for the group.
        - event_messages (Optional[bool]): Enable or disable event messages for the group.
        - chat_reaction_setting (Optional[Dict[str, Union[str, int]]]): The new chat reaction setting.
        - chat_history_for_new_members (Optional[str]): The new chat history setting for new members.

        Returns:
        - rubpy.types.Update: The result of the API call.
        """
        updated_parameters = []
        input_data = {'group_guid': group_guid}

        if title is not None:
            input_data['title'] = title
            updated_parameters.append('title')

        if description is not None:
            input_data['description'] = description
            updated_parameters.append('description')

        if slow_mode is not None:
            input_data['slow_mode'] = slow_mode
            updated_parameters.append('slow_mode')

        if event_messages is not None:
            input_data['event_messages'] = event_messages
            updated_parameters.append('event_messages')

        if chat_reaction_setting is not None:
            input_data['chat_reaction_setting'] = chat_reaction_setting
            updated_parameters.append('chat_reaction_setting')

        if chat_history_for_new_members is not None:
            if chat_history_for_new_members not in ('Hidden', 'Visible'):
                raise ValueError('`chat_history_for_new_members` argument can only be in `["Hidden", "Visible"]`.')

            input_data['chat_history_for_new_members'] = chat_history_for_new_members
            updated_parameters.append('chat_history_for_new_members')

        input_data['updated_parameters'] = updated_parameters
        return await self.builder('editGroupInfo', input=input_data)
