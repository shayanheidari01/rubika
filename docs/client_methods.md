# لیست متدهای کلاس `rubpy.Client`

| متد | نوع | امضا | توضیح |
|-----|------|-------|--------|
| `action_on_join_request` | `Instance` | `(self: 'rubpy.Client', object_guid: str, user_guid: str, action: Literal['Accept', 'Reject'] = 'Accept') -> Dict[str, Any]` | انجام عملیات بر روی درخواست عضویت (تأیید یا رد). |
| `action_on_message_reaction` | `Instance` | `(self: 'rubpy.Client', object_guid: str, message_id: str, reaction_id: int = None, action: Literal['Add', 'Remove'] = 'Add') -> rubpy.types.update.Update` | Perform actions on reactions to a specific message. |
| `action_on_sticker_set` | `Instance` | `(self: 'rubpy.Client', sticker_set_id: str, action: Literal['Add', 'Remove'] = 'Add') -> 'rubpy.types.Update'` | Add or remove a sticker set. |
| `add_address_book` | `Instance` | `(self: 'rubpy.Client', phone: str, first_name: str, last_name: str = '') -> rubpy.types.update.Update` | Adds a contact to the client's address book. |
| `add_channel` | `Instance` | `(self: 'rubpy.Client', title: str, description: str = None, member_guids: Union[str, list] = None) -> rubpy.types.update.Update` | Create a new channel and add members if specified. |
| `add_channel_members` | `Instance` | `(self: 'rubpy.Client', channel_guid: str, member_guids: Union[str, list]) -> rubpy.types.update.Update` | Add members to a channel. |
| `add_group` | `Instance` | `(self: 'rubpy.Client', title: str, member_guids: Union[str, List[str]], description: Optional[str] = None) -> rubpy.types.update.Update` | Add a new group. |
| `add_group_members` | `Instance` | `(self: 'rubpy.Client', group_guid: str, member_guids: Union[str, list]) -> 'rubpy.types.Update'` | Adds one or more members to a group. |
| `add_handler` | `Instance` | `(self: 'rubpy.Client', func: Callable, handler: Union[ForwardRef('handlers.ChatUpdates'), ForwardRef('handlers.MessageUpdates'), ForwardRef('handlers.ShowActivities'), ForwardRef('handlers.ShowNotifications'), ForwardRef('handlers.RemoveNotifications')]) -> None` | Add a handler function for updates. |
| `add_to_my_gif_set` | `Instance` | `(self: 'rubpy.Client', object_guid: str, message_id: str) -> rubpy.types.update.Update` | Adds a GIF message to the user's personal GIF set. |
| `auto_delete_message` | `Instance` | `(self: 'rubpy.Client', object_guid: str, message_id: str, time: Union[float, int]) -> rubpy.types.update.Update` | Automatically delete a message after a specified time. |
| `ban_channel_member` | `Instance` | `(self: 'rubpy.Client', channel_guid: str, member_guid: str, action: str = 'Set') -> rubpy.types.update.Update` | Ban or unban a member in a channel. |
| `ban_group_member` | `Instance` | `(self: 'rubpy.Client', group_guid: str, member_guid: str, action: Optional[str] = 'Set') -> rubpy.types.update.Update` | Ban or unban a member from a group. |
| `ban_member` | `Instance` | `(self: 'rubpy.Client', object_guid: str, member_guid: str) -> rubpy.types.update.Update` | Ban a member from a group or channel. |
| `builder` | `Instance` | `(self: 'rubpy.Client', name: str, tmp_session: bool = False, encrypt: bool = True, dict: bool = False, input: dict = None) -> Union[rubpy.types.update.Update, dict]` | Build and send a request to the Rubika API. |
| `channel_preview_by_join_link` | `Instance` | `(self: 'rubpy.Client', link: str) -> rubpy.types.update.Update` | Get a preview of a channel using its join link. |
| `check_channel_username` | `Instance` | `(self: 'rubpy.Client', username: str) -> rubpy.types.update.Update` | Check the availability of a username for a channel. |
| `check_user_username` | `Instance` | `(self: 'rubpy.Client', username: str) -> 'rubpy.types.Update'` | Check the availability of a username for a user. |
| `connect` | `Instance` | `(self: 'rubpy.Client')` | توضیحی وجود ندارد. |
| `create_channel_voice_chat` | `Instance` | `(self: 'rubpy.Client', channel_guid: str) -> rubpy.types.update.Update` | Create a voice chat for a channel. |
| `create_group_voice_chat` | `Instance` | `(self: 'rubpy.Client', group_guid: str) -> rubpy.types.update.Update` | Create a voice chat in a group. |
| `create_join_link` | `Instance` | `(self: 'rubpy.Client', object_guid: str, expire_time: Optional[int] = None, request_needed: bool = False, title: Optional[str] = None, usage_limit: int = 0) -> Dict[str, Any]` | ساخت لینک دعوت برای گروه یا کانال. |
| `create_poll` | `Instance` | `(self: 'rubpy.Client', object_guid: str, question: str, options: list, type: str = 'Regular', is_anonymous: bool = True, allows_multiple_answers: bool = True, correct_option_index: Union[int, str] = None, explanation: str = None, reply_to_message_id: Union[str, int] = 0) -> rubpy.types.update.Update` | Create a poll message with the specified parameters. |
| `delete_avatar` | `Instance` | `(self: 'rubpy.Client', object_guid: str, avatar_id: str) -> rubpy.types.update.Update` | Delete an avatar. |
| `delete_chat_history` | `Instance` | `(self: 'rubpy.Client', object_guid: str, last_message_id: Union[str, int]) -> rubpy.types.update.Update` | Delete chat history up to a certain message. |
| `delete_contact` | `Instance` | `(self: 'rubpy.Client', user_guid: str) -> rubpy.types.update.Update` | Deletes a contact from the client's address book. |
| `delete_folder` | `Instance` | `(self: 'rubpy.Client', folder_id: str) -> rubpy.types.update.Update` | Delete a folder. |
| `delete_messages` | `Instance` | `(self: 'rubpy.Client', object_guid: str, message_ids: Union[str, list], type: str = 'Global') -> rubpy.types.update.Update` | Delete specified messages associated with the given object. |
| `delete_no_access_group_chat` | `Instance` | `(self: 'rubpy.Client', group_guid: str) -> rubpy.types.update.Update` | Delete a group chat that has no access. |
| `delete_user_chat` | `Instance` | `(self: 'rubpy.Client', user_guid: str, last_deleted_message_id: Union[str, int]) -> 'rubpy.types.Update'` | Delete a user chat. |
| `discard_channel_voice_chat` | `Instance` | `(self: 'rubpy.Client', channel_guid: str, voice_chat_id: str) -> rubpy.types.update.Update` | Discard a voice chat in a channel. |
| `disconnect` | `Instance` | `(self: 'rubpy.Client') -> None` | Disconnect from the Rubpy server. |
| `download` | `Instance` | `(self: 'rubpy.Client', file_inline: 'rubpy.types.Update', save_as: str = None, chunk_size: int = 1054768, callback=None, *args, **kwargs) -> bytes` | Download a file using its file_inline information. |
| `download_profile_picture` | `Instance` | `(self: 'rubpy.Client', object_guid: str) -> bytes` | Download the profile picture of a user, group, or channel. |
| `edit_channel_info` | `Instance` | `(self: 'rubpy.Client', channel_guid: str, title: Optional[str] = None, description: Optional[str] = None, channel_type: Optional[str] = None, sign_messages: Optional[str] = None, chat_reaction_setting: Optional[dict] = None, chat_history_for_new_members: Optional[str] = None) -> rubpy.types.update.Update` | Edit information of a channel. |
| `edit_group_info` | `Instance` | `(self: 'rubpy.Client', group_guid: str, title: Optional[str] = None, description: Optional[str] = None, slow_mode: Optional[str] = None, event_messages: Optional[bool] = None, chat_reaction_setting: Optional[Dict[str, Union[str, int]]] = None, chat_history_for_new_members: Optional[str] = None) -> rubpy.types.update.Update` | Edit the information of a group. |
| `edit_message` | `Instance` | `(self: 'rubpy.Client', object_guid: str, message_id: Union[int, str], text: str, parse_mode: str = None) -> rubpy.types.update.Update` | Edit the specified message associated with the given object. |
| `forward_messages` | `Instance` | `(self: 'rubpy.Client', from_object_guid: str, to_object_guid: str, message_ids: Union[str, int, list]) -> rubpy.types.update.Update` | Forward specified messages from one object to another. |
| `get_abs_objects` | `Instance` | `(self, object_guids: Union[str, list]) -> rubpy.types.update.Update` | Get absolute objects based on their unique identifiers. |
| `get_avatars` | `Instance` | `(self: 'rubpy.Client', object_guid: str) -> rubpy.types.update.Update` | Get avatars of a specific object. |
| `get_banned_group_members` | `Instance` | `(self: 'rubpy.Client', group_guid: str, start_id: str = None) -> rubpy.types.update.Update` | Get the list of banned members in a group. |
| `get_blocked_users` | `Instance` | `(self: 'rubpy.Client') -> rubpy.types.update.Update` | Get a list of blocked users. |
| `get_channel_admin_access_list` | `Instance` | `(self: 'rubpy.Client', channel_guid: str, member_guid: str) -> rubpy.types.update.Update` | Get the admin access list for a specific member in a channel. |
| `get_channel_admin_members` | `Instance` | `(self: 'rubpy.Client', channel_guid: str, start_id: str = None) -> rubpy.types.update.Update` | Get the list of admin members in a channel. |
| `get_channel_all_members` | `Instance` | `(self: 'rubpy.Client', channel_guid: str, search_text: str = None, start_id: str = None) -> rubpy.types.update.Update` | Get all members in a channel. |
| `get_channel_info` | `Instance` | `(self: 'rubpy.Client', channel_guid: str) -> rubpy.types.update.Update` | Get information about a channel. |
| `get_channel_link` | `Instance` | `(self: 'rubpy.Client', channel_guid: str) -> rubpy.types.update.Update` | Get the join link of a channel. |
| `get_chats` | `Instance` | `(self: 'rubpy.Client', start_id: Optional[str] = None) -> rubpy.types.update.Update` | Get a list of chats. |
| `get_chats_updates` | `Instance` | `(self: 'rubpy.Client', state: Union[str, int, NoneType] = None) -> rubpy.types.update.Update` | Get updates for chats. |
| `get_contacts` | `Instance` | `(self: 'rubpy.Client', start_id: Union[str, int, NoneType] = None) -> rubpy.types.update.Update` | Get a list of contacts. |
| `get_contacts_updates` | `Instance` | `(self: 'rubpy.Client', state: Union[str, int, NoneType] = 1748352382) -> rubpy.types.update.Update` | Get updates related to contacts. |
| `get_folders` | `Instance` | `(self: 'rubpy.Client', last_state: Union[int, str] = 1748352382) -> rubpy.types.update.Update` | Get a list of folders. |
| `get_group_admin_access_list` | `Instance` | `(self: 'rubpy.Client', group_guid: str, member_guid: str) -> rubpy.types.update.Update` | Get the admin access list for a member in a group. |
| `get_group_admin_members` | `Instance` | `(self: 'rubpy.Client', group_guid: str, start_id: str = None) -> rubpy.types.update.Update` | Get the list of admin members in a group. |
| `get_group_all_members` | `Instance` | `(self: 'rubpy.Client', group_guid: str, search_text: str = None, start_id: str = None) -> rubpy.types.update.Update` | Get all members of a group. |
| `get_group_default_access` | `Instance` | `(self, group_guid: str) -> rubpy.types.update.Update` | Get the default access settings for a group. |
| `get_group_info` | `Instance` | `(self, group_guid: str) -> rubpy.types.update.Update` | Get information about a group. |
| `get_group_link` | `Instance` | `(self, group_guid: str) -> rubpy.types.update.Update` | Get the link associated with a group. |
| `get_group_mention_list` | `Instance` | `(self, group_guid: str, search_mention: str = None) -> rubpy.types.update.Update` | Get the mention list for a group. |
| `get_group_online_count` | `Instance` | `(self: 'rubpy.Client', group_guid: str)` | توضیحی وجود ندارد. |
| `get_group_voice_chat_updates` | `Instance` | `(self: 'rubpy.Client', group_guid: str, voice_chat_id: str, state: int = None) -> rubpy.types.update.Update` | Get voice chat updates for a group. |
| `get_info` | `Instance` | `(self: 'rubpy.Client', object_guid: str = None, username: str = None) -> rubpy.types.update.Update` | Get information about a user, group, or channel. |
| `get_join_links` | `Instance` | `(self: 'rubpy.Client', object_guid: str) -> dict` | دریافت لینک‌های پیوستن به یک گروه/کانال خاص بر اساس object_guid. |
| `get_join_requests` | `Instance` | `(self: 'rubpy.Client', object_guid: str) -> dict` | دریافت درخواست‌های عضویت در گروه یا کانال مشخص‌شده. |
| `get_link_from_app_url` | `Instance` | `(self: 'rubpy.Client', app_url: str) -> rubpy.types.update.Update` | Retrieves a link from an application URL. |
| `get_me` | `Instance` | `(self: 'rubpy.Client') -> 'rubpy.types.Update'` | Get information about the authenticated user. |
| `get_members` | `Instance` | `(self: 'rubpy.Client', object_guid: str, start_id: int = None, search_text: str = '') -> 'rubpy.types.Update'` | Get members of a group or channel. |
| `get_message_url` | `Instance` | `(self: 'rubpy.Client', object_guid: str, message_id: str) -> rubpy.types.update.Update` | Get the shareable URL of a specific message. |
| `get_messages_by_id` | `Instance` | `(self: 'rubpy.Client', object_guid: str, message_ids: Union[str, list]) -> rubpy.types.update.Update` | Retrieve messages by their IDs. |
| `get_messages_interval` | `Instance` | `(self: 'rubpy.Client', object_guid: str, middle_message_id: Union[int, str]) -> rubpy.types.update.Update` | Retrieve messages in an interval around a middle message ID. |
| `get_messages_updates` | `Instance` | `(self: 'rubpy.Client', object_guid: str, state: int = 1748352382) -> rubpy.types.update.Update` | Get message updates for a specific object. |
| `get_my_gif_set` | `Instance` | `(self: 'rubpy.Client') -> rubpy.types.update.Update` | Gets the user's personal GIF set. |
| `get_my_sessions` | `Instance` | `(self: 'rubpy.Client') -> rubpy.types.update.Update` | Get information about the current user's sessions. |
| `get_my_sticker_sets` | `Instance` | `(self: 'rubpy.Client') -> 'rubpy.types.Update'` | Get the sticker sets owned by the user. |
| `get_object_by_username` | `Instance` | `(self: 'rubpy.Client', username: str) -> rubpy.types.update.Update` | Get an object (user, group, or channel) by its username. |
| `get_poll_option_voters` | `Instance` | `(self: 'rubpy.Client', poll_id: str, selection_index: Union[str, int], start_id: Optional[str] = None) -> rubpy.types.update.Update` | Get voters for a specific poll option. |
| `get_poll_status` | `Instance` | `(self: 'rubpy.Client', poll_id: str) -> rubpy.types.update.Update` | Get the status of a specific poll. |
| `get_privacy_setting` | `Instance` | `(self: 'rubpy.Client') -> rubpy.types.update.Update` | Get the current user's privacy setting. |
| `get_profile_link_items` | `Instance` | `(self: 'rubpy.Client', object_guid: str) -> rubpy.types.update.Update` | Get profile link items for a given object. |
| `get_related_objects` | `Instance` | `(self: 'rubpy.Client', object_guid: str) -> rubpy.types.update.Update` | Get related objects for a given object. |
| `get_sticker_set_by_id` | `Instance` | `(self: 'rubpy.Client', sticker_set_id: str) -> 'rubpy.types.Update'` | Get a sticker set by its ID. |
| `get_stickers_by_emoji` | `Instance` | `(self: 'rubpy.Client', emoji: str, suggest_by: str = 'All') -> 'rubpy.types.Update'` | Get stickers by emoji. |
| `get_stickers_by_set_ids` | `Instance` | `(self: 'rubpy.Client', sticker_set_ids: Union[str, list]) -> rubpy.types.update.Update` | Get stickers by set IDs. |
| `get_suggested_folders` | `Instance` | `(self: 'rubpy.Client') -> rubpy.types.update.Update` | Get the suggested folders for the user. |
| `get_transcription` | `Instance` | `(self: 'rubpy.Client', message_id: Union[str, int], transcription_id: str) -> rubpy.types.update.Update` | Get transcription for a specific message. |
| `get_trend_sticker_sets` | `Instance` | `(self: 'rubpy.Client', start_id: str = None) -> rubpy.types.update.Update` | Get trending sticker sets. |
| `get_two_passcode_status` | `Instance` | `(self: 'rubpy.Client') -> rubpy.types.update.Update` | Get the two-passcode status for the user. |
| `get_updates` | `Instance` | `(self: 'rubpy.Client') -> 'rubpy.types.Update'` | Get updates from the server. |
| `get_user_info` | `Instance` | `(self: 'rubpy.Client', user_guid: str = None) -> 'rubpy.types.Update'` | Get information about a specific user. |
| `group_preview_by_join_link` | `Instance` | `(self: 'rubpy.Client', link: str) -> rubpy.types.update.Update` | Get group preview by join link. |
| `heartbeat` | `Instance` | `(self: 'rubpy.Client', chat_guid: str, voice_chat_id: str) -> None` | Continuously sends heartbeat updates for a voice chat. |
| `join_channel_action` | `Instance` | `(self: 'rubpy.Client', channel_guid: str, action: Literal['Join', 'Remove', 'Archive']) -> rubpy.types.update.Update` | Perform an action on a channel, such as joining, removing, or archiving. |
| `join_channel_by_link` | `Instance` | `(self: 'rubpy.Client', link: str) -> rubpy.types.update.Update` | Join a channel using its invite link. |
| `join_chat` | `Instance` | `(self: 'rubpy.Client', chat: str) -> rubpy.types.update.Update` | Join a chat using its identifier or link. |
| `join_group` | `Instance` | `(self: 'rubpy.Client', link: str) -> rubpy.types.update.Update` | Join a group using the provided link. |
| `join_voice_chat` | `Instance` | `(self: 'rubpy.Client', chat_guid: str, voice_chat_id: str, sdp_offer_data: str)` | Join to the group | channel voice chat. |
| `leave_group` | `Instance` | `(self: 'rubpy.Client', group_guid: str) -> rubpy.types.update.Update` | Leave a group. |
| `leave_group_voice_chat` | `Instance` | `(self: 'rubpy.Client', group_guid: str, voice_chat_id: str) -> rubpy.types.update.Update` | Leave a voice chat in a group. |
| `on_chat_updates` | `Instance` | `(self: 'rubpy.Client', *args, **kwargs)` | توضیحی وجود ندارد. |
| `on_message_updates` | `Instance` | `(self: 'rubpy.Client', *args, **kwargs)` | توضیحی وجود ندارد. |
| `on_remove_notifications` | `Instance` | `(self: 'rubpy.Client', *args, **kwargs)` | توضیحی وجود ندارد. |
| `on_show_activities` | `Instance` | `(self: 'rubpy.Client', *args, **kwargs)` | توضیحی وجود ندارد. |
| `on_show_notifications` | `Instance` | `(self: 'rubpy.Client', *args, **kwargs)` | توضیحی وجود ندارد. |
| `reaction` | `Instance` | `(self: 'rubpy.Client', object_guid: str, message_id: str, reaction_id: int) -> rubpy.types.update.Update` | Add a reaction to a specific message. |
| `register_device` | `Instance` | `(self: 'rubpy.Client', *args, **kwargs)` | توضیحی وجود ندارد. |
| `remove_channel` | `Instance` | `(self: 'rubpy.Client', channel_guid: str) -> rubpy.types.update.Update` | Remove a channel. |
| `remove_from_my_gif_set` | `Instance` | `(self: 'rubpy.Client', file_id: str) -> rubpy.types.update.Update` | Removes a GIF from the user's personal GIF set. |
| `remove_group` | `Instance` | `(self: 'rubpy.Client', group_guid: str) -> rubpy.types.update.Update` | Remove a group. |
| `remove_handler` | `Instance` | `(self: 'rubpy.Client', func) -> None` | Remove a handler function. |
| `remove_reaction` | `Instance` | `(self: 'rubpy.Client', object_guid: str, message_id: str, reaction_id: int) -> rubpy.types.update.Update` | Remove a reaction from a specific message. |
| `report_object` | `Instance` | `(self: 'rubpy.Client', object_guid: str, report_type: 'rubpy.enums.ReportType', description: str = None, message_id: str = None, report_type_object: 'rubpy.enums.ReportTypeObject' = 'Object') -> rubpy.types.update.Update` | Report an object (user, channel, group, etc.) for a specific reason. |
| `request_send_file` | `Instance` | `(self: 'rubpy.Client', file_name: str, size: Union[str, int, float], mime: str = None) -> rubpy.types.update.Update` | Request sending a file. |
| `run` | `Instance` | `(self: 'rubpy.Client', coroutine: Optional[Coroutine] = None, phone_number: str = None)` | Run the client in either synchronous or asynchronous mode. |
| `search_chat_messages` | `Instance` | `(self: 'rubpy.Client', object_guid: str, search_text: str, type: str = 'Text') -> rubpy.types.update.Update` | Searches for chat messages based on the specified criteria. |
| `search_global_objects` | `Instance` | `(self: 'rubpy.Client', search_text: str) -> rubpy.types.update.Update` | Search for global objects (users, channels, etc.) based on the given search text. |
| `search_stickers` | `Instance` | `(self: 'rubpy.Client', search_text: str = '', start_id: str = None) -> rubpy.types.update.Update` | Search for stickers. |
| `seen_channel_messages` | `Instance` | `(self: 'rubpy.Client', channel_guid: str, min_id: Union[int, str], max_id: Union[int, str]) -> rubpy.types.update.Update` | Mark channel messages as seen within a specific range. |
| `seen_chats` | `Instance` | `(self: 'rubpy.Client', seen_list: dict) -> rubpy.types.update.Update` | Marks multiple chats as seen. |
| `send_chat_activity` | `Instance` | `(self: 'rubpy.Client', object_guid: str, activity: str = 'Typing') -> rubpy.types.update.Update` | Sends a chat activity, such as typing, uploading, or recording. |
| `send_code` | `Instance` | `(self: 'rubpy.Client', phone_number: str, pass_key: Optional[str] = None, send_type: Optional[str] = 'SMS')` | توضیحی وجود ندارد. |
| `send_document` | `Instance` | `(self: 'rubpy.Client', object_guid: str, document: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, auto_delete: Optional[int] = None, *args, **kwargs) -> rubpy.types.update.Update` | Send a document. |
| `send_gif` | `Instance` | `(self: 'rubpy.Client', object_guid: str, gif: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, auto_delete: Optional[int] = None, *args, **kwargs) -> rubpy.types.update.Update` | Send a gif. |
| `send_group_voice_chat_activity` | `Instance` | `(self: 'rubpy.Client', chat_guid: str, voice_chat_id: str, participant_object_guid: str = None, activity: str = 'Speaking') -> rubpy.types.update.Update` | Set group voice chat activity. |
| `send_message` | `Instance` | `(self: 'rubpy.Client', object_guid: str, text: Optional[str] = None, reply_to_message_id: Optional[str] = None, file_inline: Union[rubpy.types.update.Update, pathlib._local.Path, bytes, NoneType] = None, sticker: Union[rubpy.types.update.Update, dict, NoneType] = None, type: str = 'File', is_spoil: bool = False, thumb: bool = True, audio_info: bool = True, auto_delete: Union[int, float, NoneType] = None, parse_mode: Union[ForwardRef('rubpy.enums.ParseMode'), str, NoneType] = None, metadata: Union[rubpy.types.update.Update, dict, NoneType] = None, *args, **kwargs) -> rubpy.types.update.Update` | Send a message with optional parameters. |
| `send_music` | `Instance` | `(self: 'rubpy.Client', object_guid: str, music: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, auto_delete: Optional[int] = None, *args, **kwargs) -> rubpy.types.update.Update` | Send a music. |
| `send_photo` | `Instance` | `(self: 'rubpy.Client', object_guid: str, photo: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, is_spoil: bool = False, auto_delete: Optional[int] = None, *args, **kwargs) -> rubpy.types.update.Update` | Send a photo. |
| `send_sticker` | `Instance` | `(self: 'rubpy.Client', object_guid: str, emoji_character: str, sticker_id: str, sticker_set_id: str, file: dict, w_h_ratio: str = '1.0', reply_to_message_id: str = None, auto_delete: int = None) -> 'rubpy.types.Update'` | Send a sticker. |
| `send_video` | `Instance` | `(self: 'rubpy.Client', object_guid: str, video: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, is_spoil: bool = False, auto_delete: Optional[int] = None, *args, **kwargs) -> 'rubpy.types.Update'` | Send a video. |
| `send_video_message` | `Instance` | `(self: 'rubpy.Client', object_guid: str, video_message: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, auto_delete: Optional[int] = None, *args, **kwargs) -> 'rubpy.types.Update'` | Send a video message. |
| `send_voice` | `Instance` | `(self: 'rubpy.Client', object_guid: str, voice: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, auto_delete: Optional[int] = None, *args, **kwargs) -> 'rubpy.types.Update'` | Send a voice. |
| `set_action_chat` | `Instance` | `(self: 'rubpy.Client', object_guid: str, action: str = 'Mute') -> rubpy.types.update.Update` | Set the action for a chat, such as muting or unmuting. |
| `set_block_user` | `Instance` | `(self: 'rubpy.Client', user_guid: str, action: Literal['Block', 'Unblock'] = 'Block') -> 'rubpy.types.Update'` | Block or unblock a user. |
| `set_channel_link` | `Instance` | `(self: 'rubpy.Client', channel_guid: str) -> rubpy.types.update.Update` | Set a custom link for the channel. |
| `set_channel_voice_chat_setting` | `Instance` | `(self: 'rubpy.Client', channel_guid: str, voice_chat_id: str, title: str = None) -> rubpy.types.update.Update` | Set the title for a voice chat in a channel. |
| `set_group_admin` | `Instance` | `(self: 'rubpy.Client', group_guid: str, member_guid: str, action: str = 'SetAdmin', access_list: Union[str, list] = []) -> rubpy.types.update.Update` | Set or unset a member as a group admin. |
| `set_group_default_access` | `Instance` | `(self: 'rubpy.Client', group_guid: str, access_list: Union[str, list]) -> rubpy.types.update.Update` | Set default access for a group. |
| `set_group_link` | `Instance` | `(self: 'rubpy.Client', group_guid: str) -> rubpy.types.update.Update` | Set private link for group. |
| `set_group_voice_chat_setting` | `Instance` | `(self: 'rubpy.Client', group_guid: str, voice_chat_id: str, title: str = None) -> rubpy.types.update.Update` | Set group voice chat setting. |
| `set_pin` | `Instance` | `(self, object_guid: str, message_id: Union[str, int]) -> rubpy.types.update.Update` | Set a pin on a message. |
| `set_pin_message` | `Instance` | `(self, object_guid: str, message_id: Union[str, int], action: Literal['Pin', 'Unpin'] = 'Pin') -> rubpy.types.update.Update` | Set or unset a pin on a message. |
| `set_setting` | `Instance` | `(self: 'rubpy.Client', show_my_last_online: str = None, show_my_phone_number: str = None, show_my_profile_photo: str = None, link_forward_message: str = None, can_join_chat_by: str = None) -> rubpy.types.update.Update` | Set various privacy settings for the user. |
| `set_unpin` | `Instance` | `(self, object_guid: str, message_id: Union[str, int]) -> rubpy.types.update.Update` | Unset a pin on a message. |
| `set_voice_chat_state` | `Instance` | `(self: 'rubpy.Client', chat_guid: str, voice_chat_id: str, participant_object_guid: str = None, action: Literal['Mute', 'Unmute'] = 'Unmute') -> rubpy.types.update.Update` | Set group or channel voice chat state. |
| `setup_two_step_verification` | `Instance` | `(self: 'rubpy.Client', password: Union[int, str], hint: str = None, recovery_email: str = None) -> rubpy.types.update.Update` | Set up two-step verification for the user. |
| `sign_in` | `Instance` | `(self: 'rubpy.Client', phone_code: str, phone_number: str, phone_code_hash: str, public_key: str) -> rubpy.types.update.Update` | توضیحی وجود ندارد. |
| `speaking` | `Instance` | `(self: 'rubpy.Client', chat_guid: str, voice_chat_id: str) -> None` | Sends voice chat activity updates. |
| `start` | `Instance` | `(self: 'rubpy.Client', phone_number: str = None)` | Start the RubPy client, handling user registration if necessary. |
| `terminate_session` | `Instance` | `(self: 'rubpy.Client', session_key: str) -> rubpy.types.update.Update` | Terminate a user session. |
| `transcribe_voice` | `Instance` | `(self: 'rubpy.Client', object_guid: str, message_id: str) -> rubpy.types.update.Update` | Transcribes voice messages. |
| `update_channel_username` | `Instance` | `(self: 'rubpy.Client', channel_guid: str, username: str) -> rubpy.types.update.Update` | Update the username of a channel. |
| `update_profile` | `Instance` | `(self: 'rubpy.Client', first_name: Optional[str] = None, last_name: Optional[str] = None, bio: Optional[str] = None) -> rubpy.types.update.Update` | Update user profile information. |
| `update_username` | `Instance` | `(self: 'rubpy.Client', username: str) -> rubpy.types.update.Update` | Update the username of the user. |
| `upload` | `Instance` | `(self: 'rubpy.Client', file, *args, **kwargs) -> 'rubpy.types.Update'` | Upload a file. |
| `upload_avatar` | `Instance` | `(self: 'rubpy.Client', object_guid: str, image: Union[pathlib._local.Path, bytes], *args, **kwargs)` | Uploads an avatar image for a specified object (user, group, or chat). |
| `user_is_admin` | `Instance` | `(self: 'rubpy.Client', object_guid: str, user_guid: str) -> bool` | Checks if a user is an admin in a group or channel. |
| `voice_chat_player` | `Instance` | `(self: 'rubpy.Client', chat_guid: str, media: 'pathlib.Path', loop: bool = False) -> bool` | Initiates a voice chat player for a given chat and media file. |
| `vote_poll` | `Instance` | `(self: 'rubpy.Client', poll_id: str, selection_index: Union[str, int]) -> rubpy.types.update.Update` | Vote on a poll option. |
