from typing import Optional
import rubpy


class SetSetting:
    async def set_setting(
            self: "rubpy.Client",
            show_my_last_online: str = None,
            show_my_phone_number: str = None,
            show_my_profile_photo: str = None,
            link_forward_message: str = None,
            can_join_chat_by: str = None,
    ):
        input = {}
        updated_parameters = []

        if isinstance(show_my_last_online, str):
            if show_my_last_online not in ('Nobody', 'Everybody', 'MyContacts'):
                raise ValueError('The `show_my_last_online` can only be in `["Nobody", "Everybody", "MyContacts"]`.')

            input['show_my_last_online'] = show_my_last_online
            updated_parameters.append('show_my_last_online')

        if isinstance(show_my_phone_number, str):
            if show_my_phone_number not in ('Nobody', 'Everybody', 'MyContacts'):
                raise ValueError('The `show_my_phone_number` can only be in `["Nobody", "Everybody", "MyContacts"]`.')

            input['show_my_phone_number'] = show_my_phone_number
            updated_parameters.append('show_my_phone_number')

        if isinstance(show_my_profile_photo, str):
            if show_my_profile_photo not in ('Everybody', 'MyContacts'):
                raise ValueError('The `show_my_profile_photo` can only be in `["Everybody", "MyContacts"]`.')

            input['show_my_profile_photo'] = show_my_profile_photo
            updated_parameters.append('show_my_profile_photo')

        if isinstance(link_forward_message, str):
            if link_forward_message not in ('Nobody', 'Everybody', 'MyContacts'):
                raise ValueError('The `link_forward_message` can only be in `["Nobody", "Everybody", "MyContacts"]`.')

            input['link_forward_message'] = link_forward_message
            updated_parameters.append('link_forward_message')

        if isinstance(can_join_chat_by, str):
            if can_join_chat_by not in ('Everybody', 'MyContacts'):
                raise ValueError('The `can_join_chat_by` can only be in `["Everybody", "MyContacts"]`.')

            input['can_join_chat_by'] = can_join_chat_by
            updated_parameters.append('can_join_chat_by')

        input['updated_parameters'] = updated_parameters

        return await self.builder(name='SetSetting', input=input)