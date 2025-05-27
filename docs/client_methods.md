# مستندات کلاس `rubpy.Client`

این سند شامل لیست متدهای عمومی و مستندات آن‌ها است.

---
## فهرست متدها

**Static Methods:**

- [action_on_join_request](#action_on_join_request)

- [action_on_message_reaction](#action_on_message_reaction)

- [action_on_sticker_set](#action_on_sticker_set)

- [add_address_book](#add_address_book)

- [add_channel](#add_channel)

- [add_channel_members](#add_channel_members)

- [add_group](#add_group)

- [add_group_members](#add_group_members)

- [add_handler](#add_handler)

- [add_to_my_gif_set](#add_to_my_gif_set)

- [auto_delete_message](#auto_delete_message)

- [ban_channel_member](#ban_channel_member)

- [ban_group_member](#ban_group_member)

- [ban_member](#ban_member)

- [builder](#builder)

- [channel_preview_by_join_link](#channel_preview_by_join_link)

- [check_channel_username](#check_channel_username)

- [check_user_username](#check_user_username)

- [connect](#connect)

- [create_channel_voice_chat](#create_channel_voice_chat)

- [create_group_voice_chat](#create_group_voice_chat)

- [create_join_link](#create_join_link)

- [create_poll](#create_poll)

- [delete_avatar](#delete_avatar)

- [delete_chat_history](#delete_chat_history)

- [delete_contact](#delete_contact)

- [delete_folder](#delete_folder)

- [delete_messages](#delete_messages)

- [delete_no_access_group_chat](#delete_no_access_group_chat)

- [delete_user_chat](#delete_user_chat)

- [discard_channel_voice_chat](#discard_channel_voice_chat)

- [disconnect](#disconnect)

- [download](#download)

- [download_profile_picture](#download_profile_picture)

- [edit_channel_info](#edit_channel_info)

- [edit_group_info](#edit_group_info)

- [edit_message](#edit_message)

- [forward_messages](#forward_messages)

- [get_abs_objects](#get_abs_objects)

- [get_avatars](#get_avatars)

- [get_banned_group_members](#get_banned_group_members)

- [get_blocked_users](#get_blocked_users)

- [get_channel_admin_access_list](#get_channel_admin_access_list)

- [get_channel_admin_members](#get_channel_admin_members)

- [get_channel_all_members](#get_channel_all_members)

- [get_channel_info](#get_channel_info)

- [get_channel_link](#get_channel_link)

- [get_chats](#get_chats)

- [get_chats_updates](#get_chats_updates)

- [get_contacts](#get_contacts)

- [get_contacts_updates](#get_contacts_updates)

- [get_folders](#get_folders)

- [get_group_admin_access_list](#get_group_admin_access_list)

- [get_group_admin_members](#get_group_admin_members)

- [get_group_all_members](#get_group_all_members)

- [get_group_default_access](#get_group_default_access)

- [get_group_info](#get_group_info)

- [get_group_link](#get_group_link)

- [get_group_mention_list](#get_group_mention_list)

- [get_group_online_count](#get_group_online_count)

- [get_group_voice_chat_updates](#get_group_voice_chat_updates)

- [get_info](#get_info)

- [get_join_links](#get_join_links)

- [get_join_requests](#get_join_requests)

- [get_link_from_app_url](#get_link_from_app_url)

- [get_me](#get_me)

- [get_members](#get_members)

- [get_message_url](#get_message_url)

- [get_messages_by_id](#get_messages_by_id)

- [get_messages_interval](#get_messages_interval)

- [get_messages_updates](#get_messages_updates)

- [get_my_gif_set](#get_my_gif_set)

- [get_my_sessions](#get_my_sessions)

- [get_my_sticker_sets](#get_my_sticker_sets)

- [get_object_by_username](#get_object_by_username)

- [get_poll_option_voters](#get_poll_option_voters)

- [get_poll_status](#get_poll_status)

- [get_privacy_setting](#get_privacy_setting)

- [get_profile_link_items](#get_profile_link_items)

- [get_related_objects](#get_related_objects)

- [get_sticker_set_by_id](#get_sticker_set_by_id)

- [get_stickers_by_emoji](#get_stickers_by_emoji)

- [get_stickers_by_set_ids](#get_stickers_by_set_ids)

- [get_suggested_folders](#get_suggested_folders)

- [get_transcription](#get_transcription)

- [get_trend_sticker_sets](#get_trend_sticker_sets)

- [get_two_passcode_status](#get_two_passcode_status)

- [get_updates](#get_updates)

- [get_user_info](#get_user_info)

- [group_preview_by_join_link](#group_preview_by_join_link)

- [heartbeat](#heartbeat)

- [join_channel_action](#join_channel_action)

- [join_channel_by_link](#join_channel_by_link)

- [join_chat](#join_chat)

- [join_group](#join_group)

- [join_voice_chat](#join_voice_chat)

- [leave_group](#leave_group)

- [leave_group_voice_chat](#leave_group_voice_chat)

- [on_chat_updates](#on_chat_updates)

- [on_message_updates](#on_message_updates)

- [on_remove_notifications](#on_remove_notifications)

- [on_show_activities](#on_show_activities)

- [on_show_notifications](#on_show_notifications)

- [reaction](#reaction)

- [register_device](#register_device)

- [remove_channel](#remove_channel)

- [remove_from_my_gif_set](#remove_from_my_gif_set)

- [remove_group](#remove_group)

- [remove_handler](#remove_handler)

- [remove_reaction](#remove_reaction)

- [report_object](#report_object)

- [request_send_file](#request_send_file)

- [run](#run)

- [search_chat_messages](#search_chat_messages)

- [search_global_objects](#search_global_objects)

- [search_stickers](#search_stickers)

- [seen_channel_messages](#seen_channel_messages)

- [seen_chats](#seen_chats)

- [send_chat_activity](#send_chat_activity)

- [send_code](#send_code)

- [send_document](#send_document)

- [send_gif](#send_gif)

- [send_group_voice_chat_activity](#send_group_voice_chat_activity)

- [send_message](#send_message)

- [send_music](#send_music)

- [send_photo](#send_photo)

- [send_sticker](#send_sticker)

- [send_video](#send_video)

- [send_video_message](#send_video_message)

- [send_voice](#send_voice)

- [set_action_chat](#set_action_chat)

- [set_block_user](#set_block_user)

- [set_channel_link](#set_channel_link)

- [set_channel_voice_chat_setting](#set_channel_voice_chat_setting)

- [set_group_admin](#set_group_admin)

- [set_group_default_access](#set_group_default_access)

- [set_group_link](#set_group_link)

- [set_group_voice_chat_setting](#set_group_voice_chat_setting)

- [set_pin](#set_pin)

- [set_pin_message](#set_pin_message)

- [set_setting](#set_setting)

- [set_unpin](#set_unpin)

- [set_voice_chat_state](#set_voice_chat_state)

- [setup_two_step_verification](#setup_two_step_verification)

- [sign_in](#sign_in)

- [speaking](#speaking)

- [start](#start)

- [terminate_session](#terminate_session)

- [transcribe_voice](#transcribe_voice)

- [update_channel_username](#update_channel_username)

- [update_profile](#update_profile)

- [update_username](#update_username)

- [upload](#upload)

- [upload_avatar](#upload_avatar)

- [user_is_admin](#user_is_admin)

- [voice_chat_player](#voice_chat_player)

- [vote_poll](#vote_poll)

---

## متدهای Static

<a name="action_on_join_request"></a>
### `action_on_join_request(self: 'rubpy.Client', object_guid: str, user_guid: str, action: Literal['Accept', 'Reject'] = 'Accept') -> Dict[str, Any]`

**نوع متد:** Static

```python
action_on_join_request(self: 'rubpy.Client', object_guid: str, user_guid: str, action: Literal['Accept', 'Reject'] = 'Accept') -> Dict[str, Any]
```

انجام عملیات بر روی درخواست عضویت (تأیید یا رد).

Args:
    object_guid (str): شناسه گروه یا کانال.
    user_guid (str): شناسه کاربری درخواست‌دهنده.
    action (Literal['Accept', 'Reject']): عملیات مورد نظر (پیش‌فرض 'Accept').

Returns:
    dict: پاسخ API پس از انجام عملیات.

Raises:
    ValueError: اگر action غیرمجاز باشد.

---
<a name="action_on_message_reaction"></a>
### `action_on_message_reaction(self: 'rubpy.Client', object_guid: str, message_id: str, reaction_id: int = None, action: Literal['Add', 'Remove'] = 'Add') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
action_on_message_reaction(self: 'rubpy.Client', object_guid: str, message_id: str, reaction_id: int = None, action: Literal['Add', 'Remove'] = 'Add') -> rubpy.types.update.Update
```

Perform actions on reactions to a specific message.

Parameters:
- object_guid (str): The GUID of the object associated with the message (e.g., user, group, channel).
- message_id (str): The ID of the message.
- reaction_id (int): The ID of the reaction.
- action (Literal['Add', 'Remove']): The action to perform on the reaction.

Returns:
- rubpy.types.Update: The updated information after performing the action on the message reaction.

---
<a name="action_on_sticker_set"></a>
### `action_on_sticker_set(self: 'rubpy.Client', sticker_set_id: str, action: Literal['Add', 'Remove'] = 'Add') -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
action_on_sticker_set(self: 'rubpy.Client', sticker_set_id: str, action: Literal['Add', 'Remove'] = 'Add') -> 'rubpy.types.Update'
```

Add or remove a sticker set.

Args:
- sticker_set_id (str): The ID of the sticker set.
- action (str, optional): The action to perform, either 'Add' or 'Remove'.

Raises:
- ValueError: If the action is not 'Add' or 'Remove'.

Returns:
- The result of the add/remove operation.

---
<a name="add_address_book"></a>
### `add_address_book(self: 'rubpy.Client', phone: str, first_name: str, last_name: str = '') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
add_address_book(self: 'rubpy.Client', phone: str, first_name: str, last_name: str = '') -> rubpy.types.update.Update
```

Adds a contact to the client's address book.

Args:
    phone (str): The phone number of the contact to be added.
    first_name (str): The first name of the contact.
    last_name (str, optional): The last name of the contact. Defaults to an empty string.

Returns:
    rubpy.types.Update: The result of the address book addition operation.

Raises:
    Any exceptions that might occur during the address book addition process.

Note:
    - The `phone` parameter should be a valid phone number.
    - The `first_name` and `last_name` parameters represent the name of the contact.
      If the contact has no last name, `last_name` can be an empty string.

---
<a name="add_channel"></a>
### `add_channel(self: 'rubpy.Client', title: str, description: str = None, member_guids: Union[str, list] = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
add_channel(self: 'rubpy.Client', title: str, description: str = None, member_guids: Union[str, list] = None) -> rubpy.types.update.Update
```

Create a new channel and add members if specified.

Parameters:
- title (str): The title of the new channel.
- description (str, optional): The description of the new channel.
- member_guids (Union[str, list], optional): The unique identifier(s) of the member(s) to be added to the new channel.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="add_channel_members"></a>
### `add_channel_members(self: 'rubpy.Client', channel_guid: str, member_guids: Union[str, list]) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
add_channel_members(self: 'rubpy.Client', channel_guid: str, member_guids: Union[str, list]) -> rubpy.types.update.Update
```

Add members to a channel.

Parameters:
- channel_guid (str): The unique identifier of the channel.
- member_guids (Union[str, list]): The unique identifier(s) of the member(s) to be added.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="add_group"></a>
### `add_group(self: 'rubpy.Client', title: str, member_guids: Union[str, List[str]], description: Optional[str] = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
add_group(self: 'rubpy.Client', title: str, member_guids: Union[str, List[str]], description: Optional[str] = None) -> rubpy.types.update.Update
```

Add a new group.

Args:
- title (str): The title of the group.
- member_guids (Union[str, List[str]]): A single member GUID or a list of member GUIDs to be added to the group.
- description (Optional[str]): Description of the group (optional).

Returns:
- rubpy.types.Update: The result of the API call.

---
<a name="add_group_members"></a>
### `add_group_members(self: 'rubpy.Client', group_guid: str, member_guids: Union[str, list]) -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
add_group_members(self: 'rubpy.Client', group_guid: str, member_guids: Union[str, list]) -> 'rubpy.types.Update'
```

Adds one or more members to a group.

Args:
    group_guid (str): The GUID of the group.
    member_guids (Union[str, list]): A single member GUID or a list of member GUIDs to be added.

Returns:
    rubpy.types.Update: An update object indicating the result of the operation.

---
<a name="add_handler"></a>
### `add_handler(self: 'rubpy.Client', func: Callable, handler: Union[ForwardRef('handlers.ChatUpdates'), ForwardRef('handlers.MessageUpdates'), ForwardRef('handlers.ShowActivities'), ForwardRef('handlers.ShowNotifications'), ForwardRef('handlers.RemoveNotifications')]) -> None`

**نوع متد:** Static

```python
add_handler(self: 'rubpy.Client', func: Callable, handler: Union[ForwardRef('handlers.ChatUpdates'), ForwardRef('handlers.MessageUpdates'), ForwardRef('handlers.ShowActivities'), ForwardRef('handlers.ShowNotifications'), ForwardRef('handlers.RemoveNotifications')]) -> None
```

Add a handler function for updates.

Args:
- func (Callable): The handler function to be added.
- handler (rubpy.handlers.Handler): The handler object.

Returns:
- None

---
<a name="add_to_my_gif_set"></a>
### `add_to_my_gif_set(self: 'rubpy.Client', object_guid: str, message_id: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
add_to_my_gif_set(self: 'rubpy.Client', object_guid: str, message_id: str) -> rubpy.types.update.Update
```

Adds a GIF message to the user's personal GIF set.

Args:
    object_guid (str): The GUID of the chat or channel.
    message_id (str): The ID of the GIF message.

---
<a name="auto_delete_message"></a>
### `auto_delete_message(self: 'rubpy.Client', object_guid: str, message_id: str, time: Union[float, int]) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
auto_delete_message(self: 'rubpy.Client', object_guid: str, message_id: str, time: Union[float, int]) -> rubpy.types.update.Update
```

Automatically delete a message after a specified time.

Parameters:
- object_guid (str): The GUID of the object associated with the message (e.g., user, group, channel).
- message_id (str): The ID of the message to be deleted.
- time (Union[float, int]): The time delay (in seconds) before deleting the message.

Returns:
- rubpy.types.Update: The updated information after deleting the message.

---
<a name="ban_channel_member"></a>
### `ban_channel_member(self: 'rubpy.Client', channel_guid: str, member_guid: str, action: str = 'Set') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
ban_channel_member(self: 'rubpy.Client', channel_guid: str, member_guid: str, action: str = 'Set') -> rubpy.types.update.Update
```

Ban or unban a member in a channel.

Parameters:
- channel_guid (str): The unique identifier of the channel.
- member_guid (str): The unique identifier of the member to be banned or unbanned.
- action (str, optional): The action to perform, can be 'Set' (ban) or 'Unset' (unban). Defaults to 'Set'.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="ban_group_member"></a>
### `ban_group_member(self: 'rubpy.Client', group_guid: str, member_guid: str, action: Optional[str] = 'Set') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
ban_group_member(self: 'rubpy.Client', group_guid: str, member_guid: str, action: Optional[str] = 'Set') -> rubpy.types.update.Update
```

Ban or unban a member from a group.

Args:
- group_guid (str): The GUID of the group.
- member_guid (str): The GUID of the member to be banned or unbanned.
- action (str): The action to perform. Should be either 'Set' (ban) or 'Unset' (unban).

Returns:
- rubpy.types.Update: The result of the API call.

Raises:
- ValueError: If the `action` argument is not 'Set' or 'Unset'.

---
<a name="ban_member"></a>
### `ban_member(self: 'rubpy.Client', object_guid: str, member_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
ban_member(self: 'rubpy.Client', object_guid: str, member_guid: str) -> rubpy.types.update.Update
```

Ban a member from a group or channel.

Args:
    object_guid (str): The GUID of the group or channel.
    member_guid (str): The GUID of the member to be banned.

Returns:
    rubpy.types.Update: The update after banning the member.

---
<a name="builder"></a>
### `builder(self: 'rubpy.Client', name: str, tmp_session: bool = False, encrypt: bool = True, dict: bool = False, input: dict = None) -> Union[rubpy.types.update.Update, dict]`

**نوع متد:** Static

```python
builder(self: 'rubpy.Client', name: str, tmp_session: bool = False, encrypt: bool = True, dict: bool = False, input: dict = None) -> Union[rubpy.types.update.Update, dict]
```

Build and send a request to the Rubika API.

Args:
    - name (str): The API method name.
    - tmp_session (bool, optional): Whether to use a temporary session. Defaults to False.
    - encrypt (bool, optional): Whether to encrypt the data. Defaults to True.
    - dict (bool, optional): Return the result as a dictionary. Defaults to False.
    - input (dict, optional): The input data for the API method. Defaults to None.

Returns:
    - Union[rubpy.types.Update, dict]: Result of the API call.

---
<a name="channel_preview_by_join_link"></a>
### `channel_preview_by_join_link(self: 'rubpy.Client', link: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
channel_preview_by_join_link(self: 'rubpy.Client', link: str) -> rubpy.types.update.Update
```

Get a preview of a channel using its join link.

Parameters:
- link (str): The join link or a link containing the channel's hash.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="check_channel_username"></a>
### `check_channel_username(self: 'rubpy.Client', username: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
check_channel_username(self: 'rubpy.Client', username: str) -> rubpy.types.update.Update
```

Check the availability of a username for a channel.

Parameters:
- username (str): The username to check.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="check_user_username"></a>
### `check_user_username(self: 'rubpy.Client', username: str) -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
check_user_username(self: 'rubpy.Client', username: str) -> 'rubpy.types.Update'
```

Check the availability of a username for a user.

Args:
- username (str): The username to be checked.

Returns:
- The result of the username availability check.

---
<a name="connect"></a>
### `connect(self: 'rubpy.Client')`

**نوع متد:** Static

```python
connect(self: 'rubpy.Client')
```

توضیحی موجود نیست.

---
<a name="create_channel_voice_chat"></a>
### `create_channel_voice_chat(self: 'rubpy.Client', channel_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
create_channel_voice_chat(self: 'rubpy.Client', channel_guid: str) -> rubpy.types.update.Update
```

Create a voice chat for a channel.

Parameters:
- channel_guid (str): The GUID of the channel.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="create_group_voice_chat"></a>
### `create_group_voice_chat(self: 'rubpy.Client', group_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
create_group_voice_chat(self: 'rubpy.Client', group_guid: str) -> rubpy.types.update.Update
```

Create a voice chat in a group.

Args:
- group_guid (str): The GUID of the group.

Returns:
- rubpy.types.Update: The result of the API call.

---
<a name="create_join_link"></a>
### `create_join_link(self: 'rubpy.Client', object_guid: str, expire_time: Optional[int] = None, request_needed: bool = False, title: Optional[str] = None, usage_limit: int = 0) -> Dict[str, Any]`

**نوع متد:** Static

```python
create_join_link(self: 'rubpy.Client', object_guid: str, expire_time: Optional[int] = None, request_needed: bool = False, title: Optional[str] = None, usage_limit: int = 0) -> Dict[str, Any]
```

ساخت لینک دعوت برای گروه یا کانال.

Args:
    object_guid (str): شناسه گروه یا کانال.
    expire_time (Optional[int]): زمان انقضا لینک به ثانیه (اختیاری).
    request_needed (bool): آیا پذیرش درخواست عضویت دستی باشد یا خیر.
    title (Optional[str]): عنوان لینک (اختیاری).
    usage_limit (int): محدودیت تعداد استفاده از لینک.

Returns:
    dict: پاسخ API شامل لینک ایجاد شده.

Raises:
    ValueError: اگر مقدار `request_needed` بولی نباشد.

---
<a name="create_poll"></a>
### `create_poll(self: 'rubpy.Client', object_guid: str, question: str, options: list, type: str = 'Regular', is_anonymous: bool = True, allows_multiple_answers: bool = True, correct_option_index: Union[int, str] = None, explanation: str = None, reply_to_message_id: Union[str, int] = 0) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
create_poll(self: 'rubpy.Client', object_guid: str, question: str, options: list, type: str = 'Regular', is_anonymous: bool = True, allows_multiple_answers: bool = True, correct_option_index: Union[int, str] = None, explanation: str = None, reply_to_message_id: Union[str, int] = 0) -> rubpy.types.update.Update
```

Create a poll message with the specified parameters.

Parameters:
- object_guid (str): The GUID of the object associated with the poll (e.g., user, group, channel).
- question (str): The question for the poll.
- options (list): A list of string values representing the poll options.
- type (str): The type of the poll, can be 'Regular' or 'Quiz'.
- is_anonymous (bool): Whether the poll is anonymous or not.
- allows_multiple_answers (bool): Whether the poll allows multiple answers or not.
- correct_option_index (Union[int, str]): The index or ID of the correct option for quiz-type polls.
- explanation (str): An explanation for the correct answer in quiz-type polls.
- reply_to_message_id (Union[str, int]): The ID of the message to reply to.

Returns:
- rubpy.types.Update: The updated information after creating the poll.

---
<a name="delete_avatar"></a>
### `delete_avatar(self: 'rubpy.Client', object_guid: str, avatar_id: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
delete_avatar(self: 'rubpy.Client', object_guid: str, avatar_id: str) -> rubpy.types.update.Update
```

Delete an avatar.

Parameters:
- object_guid (str): The unique identifier of the object (e.g., user, chat) that owns the avatar.
- avatar_id (str): The identifier of the avatar to be deleted.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="delete_chat_history"></a>
### `delete_chat_history(self: 'rubpy.Client', object_guid: str, last_message_id: Union[str, int]) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
delete_chat_history(self: 'rubpy.Client', object_guid: str, last_message_id: Union[str, int]) -> rubpy.types.update.Update
```

Delete chat history up to a certain message.

Parameters:
- object_guid (str): The unique identifier of the object (e.g., user, chat) for which chat history will be deleted.
- last_message_id (Union[str, int]): The identifier of the last message to keep in the chat history.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="delete_contact"></a>
### `delete_contact(self: 'rubpy.Client', user_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
delete_contact(self: 'rubpy.Client', user_guid: str) -> rubpy.types.update.Update
```

Deletes a contact from the client's address book.

Args:
    user_guid (str): The GUID (Globally Unique Identifier) of the contact to be deleted.

Returns:
    rubpy.types.Update: The result of the contact deletion operation.

Raises:
    Any exceptions that might occur during the contact deletion process.

Note:
    - The `user_guid` parameter should be the GUID of the contact to be deleted.

---
<a name="delete_folder"></a>
### `delete_folder(self: 'rubpy.Client', folder_id: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
delete_folder(self: 'rubpy.Client', folder_id: str) -> rubpy.types.update.Update
```

Delete a folder.

Parameters:
- folder_id (str): The ID of the folder to be deleted.

Returns:
- rubpy.types.Update: Result of the delete folder operation.

---
<a name="delete_messages"></a>
### `delete_messages(self: 'rubpy.Client', object_guid: str, message_ids: Union[str, list], type: str = 'Global') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
delete_messages(self: 'rubpy.Client', object_guid: str, message_ids: Union[str, list], type: str = 'Global') -> rubpy.types.update.Update
```

Delete specified messages associated with the given object.

Parameters:
- object_guid (str): The GUID of the object associated with the messages (e.g., user, group, channel).
- message_ids (Union[str, list]): The ID or list of IDs of the messages to be deleted.
- type (str): The type of deletion, can be 'Global' or 'Local'.

Returns:
- rubpy.types.Update: The updated information after deleting the messages.

---
<a name="delete_no_access_group_chat"></a>
### `delete_no_access_group_chat(self: 'rubpy.Client', group_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
delete_no_access_group_chat(self: 'rubpy.Client', group_guid: str) -> rubpy.types.update.Update
```

Delete a group chat that has no access.

Args:
- group_guid (str): The GUID of the group.

Returns:
- rubpy.types.Update: The result of the API call.

---
<a name="delete_user_chat"></a>
### `delete_user_chat(self: 'rubpy.Client', user_guid: str, last_deleted_message_id: Union[str, int]) -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
delete_user_chat(self: 'rubpy.Client', user_guid: str, last_deleted_message_id: Union[str, int]) -> 'rubpy.types.Update'
```

Delete a user chat.

Args:
- user_guid (str): The GUID of the user whose chat is to be deleted.
- last_deleted_message_id (Union[str, int]): The last deleted message ID.

Returns:
- The result of the user chat deletion.

---
<a name="discard_channel_voice_chat"></a>
### `discard_channel_voice_chat(self: 'rubpy.Client', channel_guid: str, voice_chat_id: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
discard_channel_voice_chat(self: 'rubpy.Client', channel_guid: str, voice_chat_id: str) -> rubpy.types.update.Update
```

Discard a voice chat in a channel.

Parameters:
- channel_guid (str): The GUID of the channel.
- voice_chat_id (str): The ID of the voice chat to discard.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="disconnect"></a>
### `disconnect(self: 'rubpy.Client') -> None`

**نوع متد:** Static

```python
disconnect(self: 'rubpy.Client') -> None
```

Disconnect from the Rubpy server.

Raises:
- exceptions.NoConnection: If the client is not connected.

---
<a name="download"></a>
### `download(self: 'rubpy.Client', file_inline: 'rubpy.types.Update', save_as: str = None, chunk_size: int = 1054768, callback=None, *args, **kwargs) -> bytes`

**نوع متد:** Static

```python
download(self: 'rubpy.Client', file_inline: 'rubpy.types.Update', save_as: str = None, chunk_size: int = 1054768, callback=None, *args, **kwargs) -> bytes
```

Download a file using its file_inline information.

Args:
- file_inline (rubpy.types.Results): The file information used for downloading.
- save_as (str, optional): The path to save the downloaded file. If None, the file will not be saved.
- chunk_size (int, optional): The size of each chunk to download.
- callback (callable, optional): A callback function to monitor the download progress.
- *args, **kwargs: Additional parameters to pass to the download method.

Returns:
- bytes: The binary data of the downloaded file.

Raises:
- aiofiles.errors.OSFError: If there is an issue with file I/O (when saving the file).

---
<a name="download_profile_picture"></a>
### `download_profile_picture(self: 'rubpy.Client', object_guid: str) -> bytes`

**نوع متد:** Static

```python
download_profile_picture(self: 'rubpy.Client', object_guid: str) -> bytes
```

Download the profile picture of a user, group, or channel.

Args:
- object_guid (str): The GUID of the user, group, channel or other chats.

Returns:
- bytes: The binary data of the profile picture.

Raises:
- rubpy.errors.ApiError: If there is an issue with the Rubpy API.

---
<a name="edit_channel_info"></a>
### `edit_channel_info(self: 'rubpy.Client', channel_guid: str, title: Optional[str] = None, description: Optional[str] = None, channel_type: Optional[str] = None, sign_messages: Optional[str] = None, chat_reaction_setting: Optional[dict] = None, chat_history_for_new_members: Optional[str] = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
edit_channel_info(self: 'rubpy.Client', channel_guid: str, title: Optional[str] = None, description: Optional[str] = None, channel_type: Optional[str] = None, sign_messages: Optional[str] = None, chat_reaction_setting: Optional[dict] = None, chat_history_for_new_members: Optional[str] = None) -> rubpy.types.update.Update
```

Edit information of a channel.

Parameters:
- channel_guid (str): The GUID of the channel.
- title (str, optional): The new title of the channel.
- description (str, optional): The new description of the channel.
- channel_type (str, optional): The new type of the channel.
- sign_messages (str, optional): Whether to sign messages in the channel.
- chat_reaction_setting (dict, optional): The new chat reaction setting.
- chat_history_for_new_members (str, optional): The chat history visibility for new members.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="edit_group_info"></a>
### `edit_group_info(self: 'rubpy.Client', group_guid: str, title: Optional[str] = None, description: Optional[str] = None, slow_mode: Optional[str] = None, event_messages: Optional[bool] = None, chat_reaction_setting: Optional[Dict[str, Union[str, int]]] = None, chat_history_for_new_members: Optional[str] = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
edit_group_info(self: 'rubpy.Client', group_guid: str, title: Optional[str] = None, description: Optional[str] = None, slow_mode: Optional[str] = None, event_messages: Optional[bool] = None, chat_reaction_setting: Optional[Dict[str, Union[str, int]]] = None, chat_history_for_new_members: Optional[str] = None) -> rubpy.types.update.Update
```

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

---
<a name="edit_message"></a>
### `edit_message(self: 'rubpy.Client', object_guid: str, message_id: Union[int, str], text: str, parse_mode: str = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
edit_message(self: 'rubpy.Client', object_guid: str, message_id: Union[int, str], text: str, parse_mode: str = None) -> rubpy.types.update.Update
```

Edit the specified message associated with the given object.

Parameters:
- object_guid (str): The GUID of the object associated with the message (e.g., user, group, channel).
- message_id (Union[int, str]): The ID of the message to be edited.
- text (str): The new text content for the message.
- parse_mode (str): The parse mode for the text, can be 'markdown' or 'html'. Defaults to None.

Returns:
- rubpy.types.Update: The updated information after editing the message.

---
<a name="forward_messages"></a>
### `forward_messages(self: 'rubpy.Client', from_object_guid: str, to_object_guid: str, message_ids: Union[str, int, list]) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
forward_messages(self: 'rubpy.Client', from_object_guid: str, to_object_guid: str, message_ids: Union[str, int, list]) -> rubpy.types.update.Update
```

Forward specified messages from one object to another.

Parameters:
- from_object_guid (str): The GUID of the source object from which messages are forwarded.
- to_object_guid (str): The GUID of the destination object to which messages are forwarded.
- message_ids (Union[str, int, list]): The IDs of the messages to be forwarded. Can be a single ID or a list of IDs.

Returns:
- rubpy.types.Update: The updated information after forwarding the messages.

---
<a name="get_abs_objects"></a>
### `get_abs_objects(self, object_guids: Union[str, list]) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_abs_objects(self, object_guids: Union[str, list]) -> rubpy.types.update.Update
```

Get absolute objects based on their unique identifiers.

Parameters:
- object_guids (Union[str, list]): The unique identifiers of the objects to retrieve.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="get_avatars"></a>
### `get_avatars(self: 'rubpy.Client', object_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_avatars(self: 'rubpy.Client', object_guid: str) -> rubpy.types.update.Update
```

Get avatars of a specific object.

Parameters:
- object_guid (str): The unique identifier of the object to retrieve avatars for.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="get_banned_group_members"></a>
### `get_banned_group_members(self: 'rubpy.Client', group_guid: str, start_id: str = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_banned_group_members(self: 'rubpy.Client', group_guid: str, start_id: str = None) -> rubpy.types.update.Update
```

Get the list of banned members in a group.

Args:
- group_guid (str): The GUID of the group.
- start_id (Optional[str]): The starting ID for fetching results.

Returns:
- rubpy.types.Update: The result of the API call.

---
<a name="get_blocked_users"></a>
### `get_blocked_users(self: 'rubpy.Client') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_blocked_users(self: 'rubpy.Client') -> rubpy.types.update.Update
```

Get a list of blocked users.

Returns:
- rubpy.types.Update: List of blocked users.

---
<a name="get_channel_admin_access_list"></a>
### `get_channel_admin_access_list(self: 'rubpy.Client', channel_guid: str, member_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_channel_admin_access_list(self: 'rubpy.Client', channel_guid: str, member_guid: str) -> rubpy.types.update.Update
```

Get the admin access list for a specific member in a channel.

Parameters:
- channel_guid (str): The GUID of the channel.
- member_guid (str): The GUID of the member.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="get_channel_admin_members"></a>
### `get_channel_admin_members(self: 'rubpy.Client', channel_guid: str, start_id: str = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_channel_admin_members(self: 'rubpy.Client', channel_guid: str, start_id: str = None) -> rubpy.types.update.Update
```

Get the list of admin members in a channel.

Parameters:
- channel_guid (str): The GUID of the channel.
- start_id (str, optional): The ID to start fetching from. Defaults to None.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="get_channel_all_members"></a>
### `get_channel_all_members(self: 'rubpy.Client', channel_guid: str, search_text: str = None, start_id: str = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_channel_all_members(self: 'rubpy.Client', channel_guid: str, search_text: str = None, start_id: str = None) -> rubpy.types.update.Update
```

Get all members in a channel.

Parameters:
- channel_guid (str): The GUID of the channel.
- search_text (str, optional): Text to search for in members. Defaults to None.
- start_id (str, optional): The ID to start fetching from. Defaults to None.

Returns:
rubpy.types.InChatMembers: The result of the API call.

---
<a name="get_channel_info"></a>
### `get_channel_info(self: 'rubpy.Client', channel_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_channel_info(self: 'rubpy.Client', channel_guid: str) -> rubpy.types.update.Update
```

Get information about a channel.

Parameters:
- channel_guid (str): The GUID of the channel.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="get_channel_link"></a>
### `get_channel_link(self: 'rubpy.Client', channel_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_channel_link(self: 'rubpy.Client', channel_guid: str) -> rubpy.types.update.Update
```

Get the join link of a channel.

Parameters:
- channel_guid (str): The GUID of the channel.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="get_chats"></a>
### `get_chats(self: 'rubpy.Client', start_id: Optional[str] = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_chats(self: 'rubpy.Client', start_id: Optional[str] = None) -> rubpy.types.update.Update
```

Get a list of chats.

Parameters:
- start_id (Optional[str]): The ID to start from. If not provided, it starts from the
  beginning.

Returns:
rubpy.types.Update: The result of the API call, representing a list of chats.

---
<a name="get_chats_updates"></a>
### `get_chats_updates(self: 'rubpy.Client', state: Union[str, int, NoneType] = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_chats_updates(self: 'rubpy.Client', state: Union[str, int, NoneType] = None) -> rubpy.types.update.Update
```

Get updates for chats.

Parameters:
- state (Optional[Union[str, int]]): State parameter for syncing updates. If not provided,
  it uses the current time minus 150 seconds.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="get_contacts"></a>
### `get_contacts(self: 'rubpy.Client', start_id: Union[str, int, NoneType] = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_contacts(self: 'rubpy.Client', start_id: Union[str, int, NoneType] = None) -> rubpy.types.update.Update
```

Get a list of contacts.

Args:
    self ("rubpy.Client"): The rubpy client.
    start_id (Optional[Union[str, int]], optional): Start ID for pagination. Defaults to None.

Returns:
    rubpy.types.Update: The result of the API call.

---
<a name="get_contacts_updates"></a>
### `get_contacts_updates(self: 'rubpy.Client', state: Union[str, int, NoneType] = 1748353902) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_contacts_updates(self: 'rubpy.Client', state: Union[str, int, NoneType] = 1748353902) -> rubpy.types.update.Update
```

Get updates related to contacts.

Args:
    self (rubpy.Client): The rubpy client.
    state (Optional[Union[str, int]], optional):
        The state parameter to filter updates. Defaults to `round(time()) - 150`.

Returns:
    rubpy.types.Update: The update related to contacts.

---
<a name="get_folders"></a>
### `get_folders(self: 'rubpy.Client', last_state: Union[int, str] = 1748353902) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_folders(self: 'rubpy.Client', last_state: Union[int, str] = 1748353902) -> rubpy.types.update.Update
```

Get a list of folders.

Parameters:
- last_state (Union[int, str]): The last state to retrieve folders.

Returns:
- rubpy.types.Update: List of folders.

---
<a name="get_group_admin_access_list"></a>
### `get_group_admin_access_list(self: 'rubpy.Client', group_guid: str, member_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_group_admin_access_list(self: 'rubpy.Client', group_guid: str, member_guid: str) -> rubpy.types.update.Update
```

Get the admin access list for a member in a group.

Args:
- group_guid (str): The GUID of the group.
- member_guid (str): The GUID of the member for whom admin access is being checked.

Returns:
- rubpy.types.Update: The result of the API call.

---
<a name="get_group_admin_members"></a>
### `get_group_admin_members(self: 'rubpy.Client', group_guid: str, start_id: str = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_group_admin_members(self: 'rubpy.Client', group_guid: str, start_id: str = None) -> rubpy.types.update.Update
```

Get the list of admin members in a group.

Args:
- group_guid (str): The GUID of the group.
- start_id (str, optional): The starting ID for pagination. Defaults to None.

Returns:
- rubpy.types.Update: The result of the API call.

---
<a name="get_group_all_members"></a>
### `get_group_all_members(self: 'rubpy.Client', group_guid: str, search_text: str = None, start_id: str = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_group_all_members(self: 'rubpy.Client', group_guid: str, search_text: str = None, start_id: str = None) -> rubpy.types.update.Update
```

Get all members of a group.

Args:
- group_guid (str): The GUID of the group.
- search_text (str, optional): Search text for filtering members. Defaults to None.
- start_id (str, optional): The starting ID for pagination. Defaults to None.

Returns:
- InChatMembers: Object containing information about the group members.

---
<a name="get_group_default_access"></a>
### `get_group_default_access(self, group_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_group_default_access(self, group_guid: str) -> rubpy.types.update.Update
```

Get the default access settings for a group.

Args:
- group_guid (str): The GUID of the group.

Returns:
- rubpy.types.Update: Update object containing information about the default access settings.

---
<a name="get_group_info"></a>
### `get_group_info(self, group_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_group_info(self, group_guid: str) -> rubpy.types.update.Update
```

Get information about a group.

Args:
- group_guid (str): The GUID of the group.

Returns:
- rubpy.types.Update: Update object containing information about the group.

---
<a name="get_group_link"></a>
### `get_group_link(self, group_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_group_link(self, group_guid: str) -> rubpy.types.update.Update
```

Get the link associated with a group.

Args:
- group_guid (str): The GUID of the group.

Returns:
- rubpy.types.Update: Update object containing the group link.

---
<a name="get_group_mention_list"></a>
### `get_group_mention_list(self, group_guid: str, search_mention: str = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_group_mention_list(self, group_guid: str, search_mention: str = None) -> rubpy.types.update.Update
```

Get the mention list for a group.

Args:
- group_guid (str): The GUID of the group.
- search_mention (str, optional): Search text for mentions.

Returns:
- rubpy.types.Update: Update object containing the group mention list.

---
<a name="get_group_online_count"></a>
### `get_group_online_count(self: 'rubpy.Client', group_guid: str)`

**نوع متد:** Static

```python
get_group_online_count(self: 'rubpy.Client', group_guid: str)
```

توضیحی موجود نیست.

---
<a name="get_group_voice_chat_updates"></a>
### `get_group_voice_chat_updates(self: 'rubpy.Client', group_guid: str, voice_chat_id: str, state: int = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_group_voice_chat_updates(self: 'rubpy.Client', group_guid: str, voice_chat_id: str, state: int = None) -> rubpy.types.update.Update
```

Get voice chat updates for a group.

Args:
- group_guid (str): The GUID of the group.
- voice_chat_id (str): The ID of the voice chat.
- state (int, optional): The state for updates. If not provided, it defaults to the current time.

Returns:
- rubpy.types.Update: Update object containing the group voice chat updates.

---
<a name="get_info"></a>
### `get_info(self: 'rubpy.Client', object_guid: str = None, username: str = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_info(self: 'rubpy.Client', object_guid: str = None, username: str = None) -> rubpy.types.update.Update
```

Get information about a user, group, or channel.

Args:
    object_guid (str, optional): The GUID of the object (user, group, or channel).
    username (str, optional): The username of the object.

Returns:
    rubpy.types.Update: The update containing information about the object.

---
<a name="get_join_links"></a>
### `get_join_links(self: 'rubpy.Client', object_guid: str) -> dict`

**نوع متد:** Static

```python
get_join_links(self: 'rubpy.Client', object_guid: str) -> dict
```

دریافت لینک‌های پیوستن به یک گروه/کانال خاص بر اساس object_guid.

Args:
    object_guid (str): شناسه گروه یا کانال

Returns:
    dict: پاسخ API شامل لینک‌های پیوستن

---
<a name="get_join_requests"></a>
### `get_join_requests(self: 'rubpy.Client', object_guid: str) -> dict`

**نوع متد:** Static

```python
get_join_requests(self: 'rubpy.Client', object_guid: str) -> dict
```

دریافت درخواست‌های عضویت در گروه یا کانال مشخص‌شده.

Args:
    object_guid (str): شناسه‌ی گروه یا کانال

Returns:
    dict: پاسخ API شامل درخواست‌های عضویت

---
<a name="get_link_from_app_url"></a>
### `get_link_from_app_url(self: 'rubpy.Client', app_url: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_link_from_app_url(self: 'rubpy.Client', app_url: str) -> rubpy.types.update.Update
```

Retrieves a link from an application URL.

Args:
    app_url (str): The application URL.

Returns:
    rubpy.types.Update: The link data.

---
<a name="get_me"></a>
### `get_me(self: 'rubpy.Client') -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
get_me(self: 'rubpy.Client') -> 'rubpy.types.Update'
```

Get information about the authenticated user.

Returns:
- Information about the authenticated user.

---
<a name="get_members"></a>
### `get_members(self: 'rubpy.Client', object_guid: str, start_id: int = None, search_text: str = '') -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
get_members(self: 'rubpy.Client', object_guid: str, start_id: int = None, search_text: str = '') -> 'rubpy.types.Update'
```

Get members of a group or channel.

Args:
- object_guid (str): The GUID of the group or channel.
- start_id (int, optional): The starting ID for fetching members.
- search_text (str, optional): The text to search for among members.

Returns:
- rubpy.types.Update: An Update object containing information about the members.

Raises:
- ValueError: If the object_guid does not start with 'c0' or 'g0'.

---
<a name="get_message_url"></a>
### `get_message_url(self: 'rubpy.Client', object_guid: str, message_id: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_message_url(self: 'rubpy.Client', object_guid: str, message_id: str) -> rubpy.types.update.Update
```

Get the shareable URL of a specific message.

Parameters:
- object_guid (str): The GUID of the object to which the message belongs.
- message_id (str): The ID of the message for which to retrieve the shareable URL.

Returns:
- rubpy.types.Update: The shareable URL of the specified message.

---
<a name="get_messages_by_id"></a>
### `get_messages_by_id(self: 'rubpy.Client', object_guid: str, message_ids: Union[str, list]) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_messages_by_id(self: 'rubpy.Client', object_guid: str, message_ids: Union[str, list]) -> rubpy.types.update.Update
```

Retrieve messages by their IDs.

Parameters:
- object_guid (str): The GUID of the object to which the messages belong.
- message_ids (Union[str, list]): The ID or list of IDs of the messages to retrieve.

Returns:
- rubpy.types.Update: The retrieved messages identified by their IDs.

---
<a name="get_messages_interval"></a>
### `get_messages_interval(self: 'rubpy.Client', object_guid: str, middle_message_id: Union[int, str]) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_messages_interval(self: 'rubpy.Client', object_guid: str, middle_message_id: Union[int, str]) -> rubpy.types.update.Update
```

Retrieve messages in an interval around a middle message ID.

Parameters:
- object_guid (str): The GUID of the object to which the messages belong.
- middle_message_id (Union[int, str]): The middle message ID around which the interval is determined.

Returns:
- rubpy.types.Update: The retrieved messages in the specified interval.

---
<a name="get_messages_updates"></a>
### `get_messages_updates(self: 'rubpy.Client', object_guid: str, state: int = 1748353902) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_messages_updates(self: 'rubpy.Client', object_guid: str, state: int = 1748353902) -> rubpy.types.update.Update
```

Get message updates for a specific object.

Parameters:
- object_guid (str): The GUID of the object for which updates are requested.
- state (int): The state at which updates are requested. Defaults to a timestamp approximately 150 seconds ago.

Returns:
- rubpy.types.Update: The message updates for the specified object.

---
<a name="get_my_gif_set"></a>
### `get_my_gif_set(self: 'rubpy.Client') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_my_gif_set(self: 'rubpy.Client') -> rubpy.types.update.Update
```

Gets the user's personal GIF set.

Returns:
    rubpy.types.Update: Information about the user's GIF set.

---
<a name="get_my_sessions"></a>
### `get_my_sessions(self: 'rubpy.Client') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_my_sessions(self: 'rubpy.Client') -> rubpy.types.update.Update
```

Get information about the current user's sessions.

Returns:
- rubpy.types.Update: Information about the user's sessions.

---
<a name="get_my_sticker_sets"></a>
### `get_my_sticker_sets(self: 'rubpy.Client') -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
get_my_sticker_sets(self: 'rubpy.Client') -> 'rubpy.types.Update'
```

Get the sticker sets owned by the user.

Returns:
- The sticker sets owned by the user.

---
<a name="get_object_by_username"></a>
### `get_object_by_username(self: 'rubpy.Client', username: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_object_by_username(self: 'rubpy.Client', username: str) -> rubpy.types.update.Update
```

Get an object (user, group, or channel) by its username.

Args:
    username (str): The username of the object.

Returns:
    rubpy.types.Update: The update containing information about the object.

---
<a name="get_poll_option_voters"></a>
### `get_poll_option_voters(self: 'rubpy.Client', poll_id: str, selection_index: Union[str, int], start_id: Optional[str] = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_poll_option_voters(self: 'rubpy.Client', poll_id: str, selection_index: Union[str, int], start_id: Optional[str] = None) -> rubpy.types.update.Update
```

Get voters for a specific poll option.

Parameters:
- poll_id (str): The ID of the poll for which voters are requested.
- selection_index (Union[str, int]): The index of the poll option for which voters are requested.
- start_id (Optional[str]): The ID from which to start fetching voters. Defaults to None.

Returns:
- rubpy.types.Update: The voters for the specified poll option.

---
<a name="get_poll_status"></a>
### `get_poll_status(self: 'rubpy.Client', poll_id: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_poll_status(self: 'rubpy.Client', poll_id: str) -> rubpy.types.update.Update
```

Get the status of a specific poll.

Parameters:
- poll_id (str): The ID of the poll for which the status is requested.

Returns:
- rubpy.types.Update: The status of the specified poll.

---
<a name="get_privacy_setting"></a>
### `get_privacy_setting(self: 'rubpy.Client') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_privacy_setting(self: 'rubpy.Client') -> rubpy.types.update.Update
```

Get the current user's privacy setting.

Returns:
- rubpy.types.Update: The current user's privacy setting.

---
<a name="get_profile_link_items"></a>
### `get_profile_link_items(self: 'rubpy.Client', object_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_profile_link_items(self: 'rubpy.Client', object_guid: str) -> rubpy.types.update.Update
```

Get profile link items for a given object.

Args:
    object_guid (str): The GUID of the object.

Returns:
    rubpy.types.Update: The update containing information about profile link items.

---
<a name="get_related_objects"></a>
### `get_related_objects(self: 'rubpy.Client', object_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_related_objects(self: 'rubpy.Client', object_guid: str) -> rubpy.types.update.Update
```

Get related objects for a given object.

Args:
    object_guid (str): The GUID of the object.

Returns:
    rubpy.types.Update: The update containing information about related objects.

---
<a name="get_sticker_set_by_id"></a>
### `get_sticker_set_by_id(self: 'rubpy.Client', sticker_set_id: str) -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
get_sticker_set_by_id(self: 'rubpy.Client', sticker_set_id: str) -> 'rubpy.types.Update'
```

Get a sticker set by its ID.

Parameters:
- sticker_set_id (str): The ID of the sticker set.

Returns:
- The sticker set corresponding to the provided ID.

---
<a name="get_stickers_by_emoji"></a>
### `get_stickers_by_emoji(self: 'rubpy.Client', emoji: str, suggest_by: str = 'All') -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
get_stickers_by_emoji(self: 'rubpy.Client', emoji: str, suggest_by: str = 'All') -> 'rubpy.types.Update'
```

Get stickers by emoji.

Parameters:
- emoji (str): The emoji character.
- suggest_by (str): The type of suggestion (default is 'All').

Returns:
- Stickers corresponding to the provided emoji and suggestion type.

---
<a name="get_stickers_by_set_ids"></a>
### `get_stickers_by_set_ids(self: 'rubpy.Client', sticker_set_ids: Union[str, list]) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_stickers_by_set_ids(self: 'rubpy.Client', sticker_set_ids: Union[str, list]) -> rubpy.types.update.Update
```

Get stickers by set IDs.

Parameters:
- sticker_set_ids (Union[str, list]): The sticker set ID or a list of sticker set IDs.

Returns:
- Stickers corresponding to the provided set IDs.

---
<a name="get_suggested_folders"></a>
### `get_suggested_folders(self: 'rubpy.Client') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_suggested_folders(self: 'rubpy.Client') -> rubpy.types.update.Update
```

Get the suggested folders for the user.

Returns:
- rubpy.types.Update: The suggested folders for the user.

---
<a name="get_transcription"></a>
### `get_transcription(self: 'rubpy.Client', message_id: Union[str, int], transcription_id: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_transcription(self: 'rubpy.Client', message_id: Union[str, int], transcription_id: str) -> rubpy.types.update.Update
```

Get transcription for a specific message.

Args:
    message_id (Union[str, int]): The ID of the message.
    transcription_id (str): The ID of the transcription.

Returns:
    rubpy.types.Update: The update containing the requested transcription.

---
<a name="get_trend_sticker_sets"></a>
### `get_trend_sticker_sets(self: 'rubpy.Client', start_id: str = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_trend_sticker_sets(self: 'rubpy.Client', start_id: str = None) -> rubpy.types.update.Update
```

Get trending sticker sets.

Parameters:
- start_id (str): The start ID for pagination.

Returns:
- Trending sticker sets.

---
<a name="get_two_passcode_status"></a>
### `get_two_passcode_status(self: 'rubpy.Client') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
get_two_passcode_status(self: 'rubpy.Client') -> rubpy.types.update.Update
```

Get the two-passcode status for the user.

Returns:
- rubpy.types.Update: The two-passcode status for the user.

---
<a name="get_updates"></a>
### `get_updates(self: 'rubpy.Client') -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
get_updates(self: 'rubpy.Client') -> 'rubpy.types.Update'
```

Get updates from the server.

Returns:
- rubpy.types.Update: An Update object containing information about the updates.

---
<a name="get_user_info"></a>
### `get_user_info(self: 'rubpy.Client', user_guid: str = None) -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
get_user_info(self: 'rubpy.Client', user_guid: str = None) -> 'rubpy.types.Update'
```

Get information about a specific user.

Args:
- user_guid (str, optional): The GUID of the user to get information about.

Returns:
- Information about the specified user.

---
<a name="group_preview_by_join_link"></a>
### `group_preview_by_join_link(self: 'rubpy.Client', link: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
group_preview_by_join_link(self: 'rubpy.Client', link: str) -> rubpy.types.update.Update
```

Get group preview by join link.

Args:
- link (str): The join link or hash link.

Returns:
- rubpy.types.Update: Update object containing the group preview information.

---
<a name="heartbeat"></a>
### `heartbeat(self: 'rubpy.Client', chat_guid: str, voice_chat_id: str) -> None`

**نوع متد:** Static

```python
heartbeat(self: 'rubpy.Client', chat_guid: str, voice_chat_id: str) -> None
```

Continuously sends heartbeat updates for a voice chat.

Args:
    chat_guid (str): The GUID of the chat.
    voice_chat_id (str): The ID of the voice chat.

---
<a name="join_channel_action"></a>
### `join_channel_action(self: 'rubpy.Client', channel_guid: str, action: Literal['Join', 'Remove', 'Archive']) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
join_channel_action(self: 'rubpy.Client', channel_guid: str, action: Literal['Join', 'Remove', 'Archive']) -> rubpy.types.update.Update
```

Perform an action on a channel, such as joining, removing, or archiving.

Parameters:
- channel_guid (str): The GUID of the channel.
- action (Literal['Join', 'Remove', 'Archive']): The action to perform on the channel.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="join_channel_by_link"></a>
### `join_channel_by_link(self: 'rubpy.Client', link: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
join_channel_by_link(self: 'rubpy.Client', link: str) -> rubpy.types.update.Update
```

Join a channel using its invite link.

Parameters:
- link (str): The invite link or hash of the channel.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="join_chat"></a>
### `join_chat(self: 'rubpy.Client', chat: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
join_chat(self: 'rubpy.Client', chat: str) -> rubpy.types.update.Update
```

Join a chat using its identifier or link.

Args:
    chat (str): The identifier or link of the chat.

Returns:
    rubpy.types.Update: The update containing information about the joined chat.

---
<a name="join_group"></a>
### `join_group(self: 'rubpy.Client', link: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
join_group(self: 'rubpy.Client', link: str) -> rubpy.types.update.Update
```

Join a group using the provided link.

Args:
- link (str): The group link or hash link.

Returns:
- rubpy.types.Update: Update object confirming the group join action.

---
<a name="join_voice_chat"></a>
### `join_voice_chat(self: 'rubpy.Client', chat_guid: str, voice_chat_id: str, sdp_offer_data: str)`

**نوع متد:** Static

```python
join_voice_chat(self: 'rubpy.Client', chat_guid: str, voice_chat_id: str, sdp_offer_data: str)
```

Join to the group | channel voice chat.

Args:
- chat_guid (str): The GUID of the Chat.
- voice_chat_id (str): The voice chat ID.
- sdp_offer_data (str): SDP offer data.

Returns:
- rubpy.types.Update: Update object confirming the change in default access.

---
<a name="leave_group"></a>
### `leave_group(self: 'rubpy.Client', group_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
leave_group(self: 'rubpy.Client', group_guid: str) -> rubpy.types.update.Update
```

Leave a group.

Args:
- group_guid (str): The GUID of the group.

Returns:
- rubpy.types.Update: Update object confirming the leave group action.

---
<a name="leave_group_voice_chat"></a>
### `leave_group_voice_chat(self: 'rubpy.Client', group_guid: str, voice_chat_id: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
leave_group_voice_chat(self: 'rubpy.Client', group_guid: str, voice_chat_id: str) -> rubpy.types.update.Update
```

Leave a voice chat in a group.

Args:
- group_guid (str): The GUID of the group.
- voice_chat_id (str): The ID of the voice chat.

Returns:
- rubpy.types.Update: Update object confirming the leave voice chat action.

---
<a name="on_chat_updates"></a>
### `on_chat_updates(self: 'rubpy.Client', *args, **kwargs)`

**نوع متد:** Static

```python
on_chat_updates(self: 'rubpy.Client', *args, **kwargs)
```

توضیحی موجود نیست.

---
<a name="on_message_updates"></a>
### `on_message_updates(self: 'rubpy.Client', *args, **kwargs)`

**نوع متد:** Static

```python
on_message_updates(self: 'rubpy.Client', *args, **kwargs)
```

توضیحی موجود نیست.

---
<a name="on_remove_notifications"></a>
### `on_remove_notifications(self: 'rubpy.Client', *args, **kwargs)`

**نوع متد:** Static

```python
on_remove_notifications(self: 'rubpy.Client', *args, **kwargs)
```

توضیحی موجود نیست.

---
<a name="on_show_activities"></a>
### `on_show_activities(self: 'rubpy.Client', *args, **kwargs)`

**نوع متد:** Static

```python
on_show_activities(self: 'rubpy.Client', *args, **kwargs)
```

توضیحی موجود نیست.

---
<a name="on_show_notifications"></a>
### `on_show_notifications(self: 'rubpy.Client', *args, **kwargs)`

**نوع متد:** Static

```python
on_show_notifications(self: 'rubpy.Client', *args, **kwargs)
```

توضیحی موجود نیست.

---
<a name="reaction"></a>
### `reaction(self: 'rubpy.Client', object_guid: str, message_id: str, reaction_id: int) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
reaction(self: 'rubpy.Client', object_guid: str, message_id: str, reaction_id: int) -> rubpy.types.update.Update
```

Add a reaction to a specific message.

Parameters:
- object_guid (str): The GUID of the object associated with the message.
- message_id (str): The ID of the message to which the reaction will be added.
- reaction_id (int): The ID of the reaction to be added.

Returns:
- rubpy.types.Update: The update indicating the success of adding the reaction.

---
<a name="register_device"></a>
### `register_device(self: 'rubpy.Client', *args, **kwargs)`

**نوع متد:** Static

```python
register_device(self: 'rubpy.Client', *args, **kwargs)
```

توضیحی موجود نیست.

---
<a name="remove_channel"></a>
### `remove_channel(self: 'rubpy.Client', channel_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
remove_channel(self: 'rubpy.Client', channel_guid: str) -> rubpy.types.update.Update
```

Remove a channel.

Parameters:
- channel_guid (str): The unique identifier of the channel.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="remove_from_my_gif_set"></a>
### `remove_from_my_gif_set(self: 'rubpy.Client', file_id: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
remove_from_my_gif_set(self: 'rubpy.Client', file_id: str) -> rubpy.types.update.Update
```

Removes a GIF from the user's personal GIF set.

Args:
    file_id (str): The file ID of the GIF to be removed.

---
<a name="remove_group"></a>
### `remove_group(self: 'rubpy.Client', group_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
remove_group(self: 'rubpy.Client', group_guid: str) -> rubpy.types.update.Update
```

Remove a group.

Args:
- group_guid (str): The GUID of the group.

Returns:
- rubpy.types.Update: Update object confirming the removal of the group.

---
<a name="remove_handler"></a>
### `remove_handler(self: 'rubpy.Client', func) -> None`

**نوع متد:** Static

```python
remove_handler(self: 'rubpy.Client', func) -> None
```

Remove a handler function.

Args:
- func: The handler function to be removed.

---
<a name="remove_reaction"></a>
### `remove_reaction(self: 'rubpy.Client', object_guid: str, message_id: str, reaction_id: int) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
remove_reaction(self: 'rubpy.Client', object_guid: str, message_id: str, reaction_id: int) -> rubpy.types.update.Update
```

Remove a reaction from a specific message.

Parameters:
- object_guid (str): The GUID of the object associated with the message.
- message_id (str): The ID of the message from which the reaction will be removed.
- reaction_id (int): The ID of the reaction to be removed.

Returns:
- rubpy.types.Update: The update indicating the success of removing the reaction.

---
<a name="report_object"></a>
### `report_object(self: 'rubpy.Client', object_guid: str, report_type: 'rubpy.enums.ReportType', description: str = None, message_id: str = None, report_type_object: 'rubpy.enums.ReportTypeObject' = 'Object') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
report_object(self: 'rubpy.Client', object_guid: str, report_type: 'rubpy.enums.ReportType', description: str = None, message_id: str = None, report_type_object: 'rubpy.enums.ReportTypeObject' = 'Object') -> rubpy.types.update.Update
```

Report an object (user, channel, group, etc.) for a specific reason.

Args:
    object_guid (str): The identifier of the object to be reported.
    report_type (rubpy.enums.ReportType): The type of report.
    description (str, optional): Additional description for the report.
    report_type_object (str, optional): The type of object being reported.

Returns:
    rubpy.types.Update: The update containing information about the report.

---
<a name="request_send_file"></a>
### `request_send_file(self: 'rubpy.Client', file_name: str, size: Union[str, int, float], mime: str = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
request_send_file(self: 'rubpy.Client', file_name: str, size: Union[str, int, float], mime: str = None) -> rubpy.types.update.Update
```

Request sending a file.

Parameters:
- file_name (str): The name of the file to be sent.
- size (Union[str, int, float]): The size of the file to be sent.
- mime (str, optional): The MIME type of the file. If None, it will be derived from the file name.

Returns:
- rubpy.types.Update: The update indicating the success of the file sending request.

---
<a name="run"></a>
### `run(self: 'rubpy.Client', coroutine: Optional[Coroutine] = None, phone_number: str = None)`

**نوع متد:** Static

```python
run(self: 'rubpy.Client', coroutine: Optional[Coroutine] = None, phone_number: str = None)
```

Run the client in either synchronous or asynchronous mode.

Args:
- coroutine (Optional[Coroutine]): An optional coroutine to run asynchronously.
- phone_number (str): The phone number to use for starting the client.

Returns:
- If running synchronously, returns the initialized client.
- If running asynchronously, returns None.

---
<a name="search_chat_messages"></a>
### `search_chat_messages(self: 'rubpy.Client', object_guid: str, search_text: str, type: str = 'Text') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
search_chat_messages(self: 'rubpy.Client', object_guid: str, search_text: str, type: str = 'Text') -> rubpy.types.update.Update
```

Searches for chat messages based on the specified criteria.

Args:
    object_guid (str): The GUID of the chat or channel.
    search_text (str): The text to search for in messages.
    type (str, optional): The type of search, can be 'Text' or 'Hashtag'. Defaults to 'Text'.

Returns:
    rubpy.types.Update: The search results.

Raises:
    ValueError: If the `type` argument is not valid.
    rubpy.exceptions.APIError: If the API request fails.

---
<a name="search_global_objects"></a>
### `search_global_objects(self: 'rubpy.Client', search_text: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
search_global_objects(self: 'rubpy.Client', search_text: str) -> rubpy.types.update.Update
```

Search for global objects (users, channels, etc.) based on the given search text.

Args:
    search_text (str): The text to search for.

Returns:
    rubpy.types.Update: The update containing search results.

---
<a name="search_stickers"></a>
### `search_stickers(self: 'rubpy.Client', search_text: str = '', start_id: str = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
search_stickers(self: 'rubpy.Client', search_text: str = '', start_id: str = None) -> rubpy.types.update.Update
```

Search for stickers.

Parameters:
- search_text (str): The search text.
- start_id (str): The start ID for pagination.

Returns:
- Stickers matching the search criteria.

---
<a name="seen_channel_messages"></a>
### `seen_channel_messages(self: 'rubpy.Client', channel_guid: str, min_id: Union[int, str], max_id: Union[int, str]) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
seen_channel_messages(self: 'rubpy.Client', channel_guid: str, min_id: Union[int, str], max_id: Union[int, str]) -> rubpy.types.update.Update
```

Mark channel messages as seen within a specific range.

Parameters:
- channel_guid (str): The unique identifier of the channel.
- min_id (Union[int, str]): The minimum message ID to mark as seen.
- max_id (Union[int, str]): The maximum message ID to mark as seen.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="seen_chats"></a>
### `seen_chats(self: 'rubpy.Client', seen_list: dict) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
seen_chats(self: 'rubpy.Client', seen_list: dict) -> rubpy.types.update.Update
```

Marks multiple chats as seen.

Args:
    seen_list (dict): A dictionary containing chat GUIDs and their last seen message IDs.

Returns:
    rubpy.types.Update: The result of the operation.

---
<a name="send_chat_activity"></a>
### `send_chat_activity(self: 'rubpy.Client', object_guid: str, activity: str = 'Typing') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
send_chat_activity(self: 'rubpy.Client', object_guid: str, activity: str = 'Typing') -> rubpy.types.update.Update
```

Sends a chat activity, such as typing, uploading, or recording.

Args:
    object_guid (str): The GUID of the chat.
    activity (str, optional): The type of activity. Defaults to 'Typing'.

Returns:
    rubpy.types.Update: The result of the operation.

Raises:
    ValueError: If the `activity` argument is not one of `["Typing", "Uploading", "Recording"]`.

---
<a name="send_code"></a>
### `send_code(self: 'rubpy.Client', phone_number: str, pass_key: Optional[str] = None, send_type: Optional[str] = 'SMS')`

**نوع متد:** Static

```python
send_code(self: 'rubpy.Client', phone_number: str, pass_key: Optional[str] = None, send_type: Optional[str] = 'SMS')
```

توضیحی موجود نیست.

---
<a name="send_document"></a>
### `send_document(self: 'rubpy.Client', object_guid: str, document: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, auto_delete: Optional[int] = None, *args, **kwargs) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
send_document(self: 'rubpy.Client', object_guid: str, document: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, auto_delete: Optional[int] = None, *args, **kwargs) -> rubpy.types.update.Update
```

Send a document.

Parameters:
- object_guid (str): The GUID of the recipient.
- document (Union[Path, bytes]): The document data.
- caption (Optional[str]): The caption for the document. Defaults to None.
- reply_to_message_id (Optional[str]): The ID of the message to which this is a reply. Defaults to None.
- auto_delete (Optional[int]): Auto-delete duration in seconds. Defaults to None.

Returns:
- rubpy.types.Update: The update indicating the success of the document sending.

---
<a name="send_gif"></a>
### `send_gif(self: 'rubpy.Client', object_guid: str, gif: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, auto_delete: Optional[int] = None, *args, **kwargs) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
send_gif(self: 'rubpy.Client', object_guid: str, gif: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, auto_delete: Optional[int] = None, *args, **kwargs) -> rubpy.types.update.Update
```

Send a gif.

Args:
    object_guid (str):
        The GUID of the recipient.

    gif (Path, bytes):
        The gif data.

    caption (str, optional):
        The caption for the gif. Defaults to None.

    reply_to_message_id (str, optional):
        The ID of the message to which this is a reply. Defaults to None.

    auto_delete (int, optional):
        Auto-delete duration in seconds. Defaults to None.

---
<a name="send_group_voice_chat_activity"></a>
### `send_group_voice_chat_activity(self: 'rubpy.Client', chat_guid: str, voice_chat_id: str, participant_object_guid: str = None, activity: str = 'Speaking') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
send_group_voice_chat_activity(self: 'rubpy.Client', chat_guid: str, voice_chat_id: str, participant_object_guid: str = None, activity: str = 'Speaking') -> rubpy.types.update.Update
```

Set group voice chat activity.

Args:
- chat_guid (str): The GUID of the Chat.
- voice_chat_id (str): The voice chat ID.
- participant_object_guid (str): Participant object guid, Defualt is `self.guid`.
- activity (str): Literal['Speaking'] and Defualt is `Speaking`.

Returns:
- rubpy.types.Update: Update object confirming the change in default access.

---
<a name="send_message"></a>
### `send_message(self: 'rubpy.Client', object_guid: str, text: Optional[str] = None, reply_to_message_id: Optional[str] = None, file_inline: Union[rubpy.types.update.Update, pathlib._local.Path, bytes, NoneType] = None, sticker: Union[rubpy.types.update.Update, dict, NoneType] = None, type: str = 'File', is_spoil: bool = False, thumb: bool = True, audio_info: bool = True, auto_delete: Union[int, float, NoneType] = None, parse_mode: Union[ForwardRef('rubpy.enums.ParseMode'), str, NoneType] = None, metadata: Union[rubpy.types.update.Update, dict, NoneType] = None, *args, **kwargs) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
send_message(self: 'rubpy.Client', object_guid: str, text: Optional[str] = None, reply_to_message_id: Optional[str] = None, file_inline: Union[rubpy.types.update.Update, pathlib._local.Path, bytes, NoneType] = None, sticker: Union[rubpy.types.update.Update, dict, NoneType] = None, type: str = 'File', is_spoil: bool = False, thumb: bool = True, audio_info: bool = True, auto_delete: Union[int, float, NoneType] = None, parse_mode: Union[ForwardRef('rubpy.enums.ParseMode'), str, NoneType] = None, metadata: Union[rubpy.types.update.Update, dict, NoneType] = None, *args, **kwargs) -> rubpy.types.update.Update
```

Send a message with optional parameters.

Parameters:
- object_guid (str): The GUID of the recipient.
- text (Optional[str]): The text of the message. Defaults to None.
- reply_to_message_id (Optional[str]): The ID of the message to which this is a reply. Defaults to None.
- file_inline (Optional[Union[Update, Path, bytes]]): The file to be sent inline with the message. Defaults to None.
- sticker (Optional[Union[Update, dict]]): The sticker to be sent with the message. Defaults to None.
- type (str): The type of the message, e.g., 'File', 'Music', 'Voice', etc. Defaults to 'File'.
- is_spoil (bool): Whether the message should be marked as a spoiler. Defaults to False.
- thumb (bool): Whether to include a thumbnail. Defaults to True.
- auto_delete (Optional[Union[int, float]]): Auto-delete duration in seconds. Defaults to None.
- parse_mode (Optional[Union[ParseMode, str]]): The parse mode for the text. Defaults to None.
- args, kwargs: Additional arguments and keyword arguments.

Returns:
- rubpy.types.Update: The update indicating the success of the message sending.

---
<a name="send_music"></a>
### `send_music(self: 'rubpy.Client', object_guid: str, music: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, auto_delete: Optional[int] = None, *args, **kwargs) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
send_music(self: 'rubpy.Client', object_guid: str, music: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, auto_delete: Optional[int] = None, *args, **kwargs) -> rubpy.types.update.Update
```

Send a music.

Args:
    object_guid (str):
        The GUID of the recipient.

    music (Path, bytes):
        The music data.

    caption (str, optional):
        The caption for the music. Defaults to None.

    reply_to_message_id (str, optional):
        The ID of the message to which this is a reply. Defaults to None.

    auto_delete (int, optional):
        Auto-delete duration in seconds. Defaults to None.

---
<a name="send_photo"></a>
### `send_photo(self: 'rubpy.Client', object_guid: str, photo: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, is_spoil: bool = False, auto_delete: Optional[int] = None, *args, **kwargs) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
send_photo(self: 'rubpy.Client', object_guid: str, photo: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, is_spoil: bool = False, auto_delete: Optional[int] = None, *args, **kwargs) -> rubpy.types.update.Update
```

Send a photo.

Args:
    object_guid (str):
        The GUID of the recipient.

    photo (Path, bytes):
        The photo data.

    caption (str, optional):
        The caption for the photo. Defaults to None.

    reply_to_message_id (str, optional):
        The ID of the message to which this is a reply. Defaults to None.

    is_spoil (bool, optional):
        Whether the photo should be marked as a spoiler. Defaults to False.

    auto_delete (int, optional):
        Auto-delete duration in seconds. Defaults to None.

---
<a name="send_sticker"></a>
### `send_sticker(self: 'rubpy.Client', object_guid: str, emoji_character: str, sticker_id: str, sticker_set_id: str, file: dict, w_h_ratio: str = '1.0', reply_to_message_id: str = None, auto_delete: int = None) -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
send_sticker(self: 'rubpy.Client', object_guid: str, emoji_character: str, sticker_id: str, sticker_set_id: str, file: dict, w_h_ratio: str = '1.0', reply_to_message_id: str = None, auto_delete: int = None) -> 'rubpy.types.Update'
```

Send a sticker.

Args:
    - object_guid (str):
        The GUID of the recipient.

    - emoji_character (str):
        The emoji character associated with the sticker.

    - sticker_id (str):
        The ID of the sticker.

    - sticker_set_id (str):
        The ID of the sticker set.

    - file (dict):
        The file data for the sticker.

    - w_h_ratio (str, optional):
        The width-to-height ratio of the sticker. Defaults to '1.0'.

    - reply_to_message_id (str, optional):
        The ID of the message to which this is a reply. Defaults to None.

    - auto_delete (int, optional):
        Auto-delete duration in seconds. Defaults to None.

---
<a name="send_video"></a>
### `send_video(self: 'rubpy.Client', object_guid: str, video: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, is_spoil: bool = False, auto_delete: Optional[int] = None, *args, **kwargs) -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
send_video(self: 'rubpy.Client', object_guid: str, video: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, is_spoil: bool = False, auto_delete: Optional[int] = None, *args, **kwargs) -> 'rubpy.types.Update'
```

Send a video.

Args:
    - object_guid (str):
        The GUID of the recipient.

    - video (Union[Path, bytes]):
        The video data.

    - caption (str, optional):
        The caption for the video. Defaults to None.

    - reply_to_message_id (str, optional):
        The ID of the message to which this is a reply. Defaults to None.

---
<a name="send_video_message"></a>
### `send_video_message(self: 'rubpy.Client', object_guid: str, video_message: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, auto_delete: Optional[int] = None, *args, **kwargs) -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
send_video_message(self: 'rubpy.Client', object_guid: str, video_message: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, auto_delete: Optional[int] = None, *args, **kwargs) -> 'rubpy.types.Update'
```

Send a video message.

Args:
    - object_guid (str):
        The GUID of the recipient.

    - video_message (Union[Path, bytes]):
        The video message data.

    - caption (str, optional):
        The caption for the video message. Defaults to None.

    - reply_to_message_id (str, optional):
        The ID of the message to which this is a reply. Defaults to None.

    - auto_delete (int, optional):
        Auto-delete duration in seconds. Defaults to None.

---
<a name="send_voice"></a>
### `send_voice(self: 'rubpy.Client', object_guid: str, voice: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, auto_delete: Optional[int] = None, *args, **kwargs) -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
send_voice(self: 'rubpy.Client', object_guid: str, voice: Union[pathlib._local.Path, bytes], caption: Optional[str] = None, reply_to_message_id: Optional[str] = None, auto_delete: Optional[int] = None, *args, **kwargs) -> 'rubpy.types.Update'
```

Send a voice.

Args:
    object_guid (str):
        The GUID of the recipient.

    voice (Union[Path, bytes]):
        The voice data.

    caption (str, optional):
        The caption for the voice. Defaults to None.

    reply_to_message_id (str, optional):
        The ID of the message to which this is a reply. Defaults to None.

---
<a name="set_action_chat"></a>
### `set_action_chat(self: 'rubpy.Client', object_guid: str, action: str = 'Mute') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
set_action_chat(self: 'rubpy.Client', object_guid: str, action: str = 'Mute') -> rubpy.types.update.Update
```

Set the action for a chat, such as muting or unmuting.

Args:
    object_guid (str): The GUID of the chat.
    action (str, optional): The action to be set. Defaults to 'Mute'.

Returns:
    rubpy.types.Update: The result of the operation.

Raises:
    ValueError: If the `action` argument is not one of `["Mute", "Unmute"]`.

---
<a name="set_block_user"></a>
### `set_block_user(self: 'rubpy.Client', user_guid: str, action: Literal['Block', 'Unblock'] = 'Block') -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
set_block_user(self: 'rubpy.Client', user_guid: str, action: Literal['Block', 'Unblock'] = 'Block') -> 'rubpy.types.Update'
```

Block or unblock a user.

Args:
- user_guid (str): The GUID of the user to block or unblock.
- action (Literal['Block', 'Unblock'], optional): The action to perform, either 'Block' or 'Unblock'.

Raises:
- ValueError: If the action is not 'Block' or 'Unblock'.

Returns:
- The result of the block/unblock operation.

---
<a name="set_channel_link"></a>
### `set_channel_link(self: 'rubpy.Client', channel_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
set_channel_link(self: 'rubpy.Client', channel_guid: str) -> rubpy.types.update.Update
```

Set a custom link for the channel.

Parameters:
- channel_guid (str): The unique identifier of the channel.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="set_channel_voice_chat_setting"></a>
### `set_channel_voice_chat_setting(self: 'rubpy.Client', channel_guid: str, voice_chat_id: str, title: str = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
set_channel_voice_chat_setting(self: 'rubpy.Client', channel_guid: str, voice_chat_id: str, title: str = None) -> rubpy.types.update.Update
```

Set the title for a voice chat in a channel.

Parameters:
- channel_guid (str): The unique identifier of the channel.
- voice_chat_id (str): The unique identifier of the voice chat.
- title (str, optional): The new title for the voice chat.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="set_group_admin"></a>
### `set_group_admin(self: 'rubpy.Client', group_guid: str, member_guid: str, action: str = 'SetAdmin', access_list: Union[str, list] = []) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
set_group_admin(self: 'rubpy.Client', group_guid: str, member_guid: str, action: str = 'SetAdmin', access_list: Union[str, list] = []) -> rubpy.types.update.Update
```

Set or unset a member as a group admin.

Args:
- group_guid (str): The GUID of the group.
- member_guid (str): The GUID of the member.
- action (str): The action to perform, either 'SetAdmin' or 'UnsetAdmin'.
- access_list (Union[str, list]): List of allowed actions. Default is an empty list.

Returns:
- rubpy.types.Update: Update object confirming the change in admin status.

---
<a name="set_group_default_access"></a>
### `set_group_default_access(self: 'rubpy.Client', group_guid: str, access_list: Union[str, list]) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
set_group_default_access(self: 'rubpy.Client', group_guid: str, access_list: Union[str, list]) -> rubpy.types.update.Update
```

Set default access for a group.

Args:
- group_guid (str): The GUID of the group.
- access_list (Union[str, list]): List of allowed actions.

Returns:
- rubpy.types.Update: Update object confirming the change in default access.

---
<a name="set_group_link"></a>
### `set_group_link(self: 'rubpy.Client', group_guid: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
set_group_link(self: 'rubpy.Client', group_guid: str) -> rubpy.types.update.Update
```

Set private link for group.

Args:
- group_guid (str): The GUID of the group.

Returns:
- rubpy.types.Update: Update object confirming the change in default access.

---
<a name="set_group_voice_chat_setting"></a>
### `set_group_voice_chat_setting(self: 'rubpy.Client', group_guid: str, voice_chat_id: str, title: str = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
set_group_voice_chat_setting(self: 'rubpy.Client', group_guid: str, voice_chat_id: str, title: str = None) -> rubpy.types.update.Update
```

Set group voice chat setting.

Args:
- group_guid (str): The GUID of the group.
- voice_chat_id (str): The voice chat ID.
- title (str): Title of voice chat, Defualt is None.

Returns:
- rubpy.types.Update: Update object confirming the change in default access.

---
<a name="set_pin"></a>
### `set_pin(self, object_guid: str, message_id: Union[str, int]) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
set_pin(self, object_guid: str, message_id: Union[str, int]) -> rubpy.types.update.Update
```

Set a pin on a message.

Args:
    - object_guid (str): The GUID of the recipient.
    - message_id (Union[str, int]): The ID of the message to pin.

Returns:
    - rubpy.types.Update: The update indicating the success of setting the pin.

---
<a name="set_pin_message"></a>
### `set_pin_message(self, object_guid: str, message_id: Union[str, int], action: Literal['Pin', 'Unpin'] = 'Pin') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
set_pin_message(self, object_guid: str, message_id: Union[str, int], action: Literal['Pin', 'Unpin'] = 'Pin') -> rubpy.types.update.Update
```

Set or unset a pin on a message.

Args:
    - object_guid (str): The GUID of the recipient.
    - message_id (Union[str, int]): The ID of the message to pin or unpin.
    - action (Literal['Pin', 'Unpin']): The action to perform, either 'Pin' or 'Unpin'.

Returns:
    - rubpy.types.Update: The update indicating the success of the operation.

---
<a name="set_setting"></a>
### `set_setting(self: 'rubpy.Client', show_my_last_online: str = None, show_my_phone_number: str = None, show_my_profile_photo: str = None, link_forward_message: str = None, can_join_chat_by: str = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
set_setting(self: 'rubpy.Client', show_my_last_online: str = None, show_my_phone_number: str = None, show_my_profile_photo: str = None, link_forward_message: str = None, can_join_chat_by: str = None) -> rubpy.types.update.Update
```

Set various privacy settings for the user.

Parameters:
- show_my_last_online (Optional[str]): Privacy setting for showing last online status.
- show_my_phone_number (Optional[str]): Privacy setting for showing phone number.
- show_my_profile_photo (Optional[str]): Privacy setting for showing profile photo.
- link_forward_message (Optional[str]): Privacy setting for link forwarding messages.
- can_join_chat_by (Optional[str]): Privacy setting for who can join chats.

Returns:
- rubpy.types.Update: The updated privacy settings.

---
<a name="set_unpin"></a>
### `set_unpin(self, object_guid: str, message_id: Union[str, int]) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
set_unpin(self, object_guid: str, message_id: Union[str, int]) -> rubpy.types.update.Update
```

Unset a pin on a message.

Args:
    - object_guid (str): The GUID of the recipient.
    - message_id (Union[str, int]): The ID of the message to unpin.

Returns:
    - rubpy.types.Update: The update indicating the success of unsetting the pin.

---
<a name="set_voice_chat_state"></a>
### `set_voice_chat_state(self: 'rubpy.Client', chat_guid: str, voice_chat_id: str, participant_object_guid: str = None, action: Literal['Mute', 'Unmute'] = 'Unmute') -> rubpy.types.update.Update`

**نوع متد:** Static

```python
set_voice_chat_state(self: 'rubpy.Client', chat_guid: str, voice_chat_id: str, participant_object_guid: str = None, action: Literal['Mute', 'Unmute'] = 'Unmute') -> rubpy.types.update.Update
```

Set group or channel voice chat state.

Args:
- chat_guid (str): The GUID of the Chat.
- voice_chat_id (str): The voice chat ID.
- participant_object_guid (str): Participant object guid, Defualt is `self.guid`.
- action (str): Literal['Mute', 'Unmute'] and Defualt is `Unmute`.

Returns:
- rubpy.types.Update: Update object confirming the change in default access.

---
<a name="setup_two_step_verification"></a>
### `setup_two_step_verification(self: 'rubpy.Client', password: Union[int, str], hint: str = None, recovery_email: str = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
setup_two_step_verification(self: 'rubpy.Client', password: Union[int, str], hint: str = None, recovery_email: str = None) -> rubpy.types.update.Update
```

Set up two-step verification for the user.

Parameters:
- password (Union[int, str]): The current user password.
- hint (str): A hint to help remember the password.
- recovery_email (str): The recovery email for two-step verification.

Returns:
- rubpy.types.Update: The updated user information after setting up two-step verification.

---
<a name="sign_in"></a>
### `sign_in(self: 'rubpy.Client', phone_code: str, phone_number: str, phone_code_hash: str, public_key: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
sign_in(self: 'rubpy.Client', phone_code: str, phone_number: str, phone_code_hash: str, public_key: str) -> rubpy.types.update.Update
```

توضیحی موجود نیست.

---
<a name="speaking"></a>
### `speaking(self: 'rubpy.Client', chat_guid: str, voice_chat_id: str) -> None`

**نوع متد:** Static

```python
speaking(self: 'rubpy.Client', chat_guid: str, voice_chat_id: str) -> None
```

Sends voice chat activity updates.

Args:
    chat_guid (str): The GUID of the chat.
    voice_chat_id (str): The ID of the voice chat.

---
<a name="start"></a>
### `start(self: 'rubpy.Client', phone_number: str = None)`

**نوع متد:** Static

```python
start(self: 'rubpy.Client', phone_number: str = None)
```

Start the RubPy client, handling user registration if necessary.

Args:
- phone_number (str): The phone number to use for starting the client.

Returns:
- The initialized client.

---
<a name="terminate_session"></a>
### `terminate_session(self: 'rubpy.Client', session_key: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
terminate_session(self: 'rubpy.Client', session_key: str) -> rubpy.types.update.Update
```

Terminate a user session.

Parameters:
- session_key (str): The session key of the session to be terminated.

Returns:
- rubpy.types.Update: The updated user information after terminating the session.

---
<a name="transcribe_voice"></a>
### `transcribe_voice(self: 'rubpy.Client', object_guid: str, message_id: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
transcribe_voice(self: 'rubpy.Client', object_guid: str, message_id: str) -> rubpy.types.update.Update
```

Transcribes voice messages.

Parameters:
    - object_guid (str): The GUID of the object (chat, channel, or group) containing the voice message.
    - message_id (str): The ID of the voice message.

Returns:
    rubpy.types.Update: The transcription result.

---
<a name="update_channel_username"></a>
### `update_channel_username(self: 'rubpy.Client', channel_guid: str, username: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
update_channel_username(self: 'rubpy.Client', channel_guid: str, username: str) -> rubpy.types.update.Update
```

Update the username of a channel.

Parameters:
- channel_guid (str): The unique identifier of the channel.
- username (str): The new username for the channel.

Returns:
rubpy.types.Update: The result of the API call.

---
<a name="update_profile"></a>
### `update_profile(self: 'rubpy.Client', first_name: Optional[str] = None, last_name: Optional[str] = None, bio: Optional[str] = None) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
update_profile(self: 'rubpy.Client', first_name: Optional[str] = None, last_name: Optional[str] = None, bio: Optional[str] = None) -> rubpy.types.update.Update
```

Update user profile information.

Parameters:
- first_name (Optional[str]): The updated first name.
- last_name (Optional[str]): The updated last name.
- bio (Optional[str]): The updated biography.

Returns:
- rubpy.types.Update: The updated user information after the profile update.

---
<a name="update_username"></a>
### `update_username(self: 'rubpy.Client', username: str) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
update_username(self: 'rubpy.Client', username: str) -> rubpy.types.update.Update
```

Update the username of the user.

Parameters:
- username (str): The new username for the user.

Returns:
- rubpy.types.Update: The updated user information after the username update.

---
<a name="upload"></a>
### `upload(self: 'rubpy.Client', file, *args, **kwargs) -> 'rubpy.types.Update'`

**نوع متد:** Static

```python
upload(self: 'rubpy.Client', file, *args, **kwargs) -> 'rubpy.types.Update'
```

Upload a file.

Args:
- file: The file to be uploaded.
- *args: Additional positional arguments.
- **kwargs: Additional keyword arguments.

Returns:
- The result of the file upload operation.

---
<a name="upload_avatar"></a>
### `upload_avatar(self: 'rubpy.Client', object_guid: str, image: Union[pathlib._local.Path, bytes], *args, **kwargs)`

**نوع متد:** Static

```python
upload_avatar(self: 'rubpy.Client', object_guid: str, image: Union[pathlib._local.Path, bytes], *args, **kwargs)
```

Uploads an avatar image for a specified object (user, group, or chat).

Args:
    object_guid (str): The GUID of the object for which the avatar is being uploaded.
    image (Union[Path, bytes]): The image file or bytes to be used as the avatar.
    *args, **kwargs: Additional arguments to be passed to the `upload` method.

Returns:
    rubpy.types.Update: The result of the avatar upload operation.

Raises:
    Any exceptions that might occur during the avatar upload process.

Note:
    - If `object_guid` is 'me', 'cloud', or 'self', it will be replaced with the client's GUID.
    - If `image` is a string (path to a file), the file name is extracted from the path.
      Otherwise, a default file name ('rubpy.jpg') is used.
    - The `upload` method is used internally to handle the file upload process.

---
<a name="user_is_admin"></a>
### `user_is_admin(self: 'rubpy.Client', object_guid: str, user_guid: str) -> bool`

**نوع متد:** Static

```python
user_is_admin(self: 'rubpy.Client', object_guid: str, user_guid: str) -> bool
```

Checks if a user is an admin in a group or channel.

Args:
    object_guid (str): The GUID of the group or channel.
    user_guid (str): The GUID of the user.

Returns:
    bool: True if the user is an admin, False otherwise.

---
<a name="voice_chat_player"></a>
### `voice_chat_player(self: 'rubpy.Client', chat_guid: str, media: 'pathlib.Path', loop: bool = False) -> bool`

**نوع متد:** Static

```python
voice_chat_player(self: 'rubpy.Client', chat_guid: str, media: 'pathlib.Path', loop: bool = False) -> bool
```

Initiates a voice chat player for a given chat and media file.

Args:
    chat_guid (str): The GUID of the chat.
    media (pathlib.Path): The path to the media file.
    loop (bool, optional): Whether to loop the media. Defaults to False.

Returns:
    bool: True if the voice chat player is initiated successfully, False otherwise.

---
<a name="vote_poll"></a>
### `vote_poll(self: 'rubpy.Client', poll_id: str, selection_index: Union[str, int]) -> rubpy.types.update.Update`

**نوع متد:** Static

```python
vote_poll(self: 'rubpy.Client', poll_id: str, selection_index: Union[str, int]) -> rubpy.types.update.Update
```

Vote on a poll option.

Args:
    poll_id (str): The ID of the poll.
    selection_index (Union[str, int]): The index of the option to vote for.

Returns:
    rubpy.types.Update: The update indicating the success of the vote.

---

*مستندات به‌صورت خودکار تولید شده‌اند.*