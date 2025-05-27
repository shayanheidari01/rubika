# مستندات کلاس `rubpy.Client`

این سند شامل لیست متدهای عمومی و مستندات آن‌ها است.

---
## فهرست متدها

**Static Methods:**

- [ban_member](#ban_member)

- [block](#block)

- [copy](#copy)

- [delete](#delete)

- [delete_messages](#delete_messages)

- [download](#download)

- [edit](#edit)

- [find_keys](#find_keys)

- [forward](#forward)

- [forwards](#forwards)

- [get_author](#get_author)

- [get_messages](#get_messages)

- [get_object](#get_object)

- [get_reply_author](#get_reply_author)

- [get_reply_message](#get_reply_message)

- [guid_type](#guid_type)

- [is_admin](#is_admin)

- [jsonify](#jsonify)

- [pin](#pin)

- [reaction](#reaction)

- [reply](#reply)

- [reply_document](#reply_document)

- [reply_gif](#reply_gif)

- [reply_music](#reply_music)

- [reply_photo](#reply_photo)

- [reply_video](#reply_video)

- [reply_video_message](#reply_video_message)

- [reply_voice](#reply_voice)

- [seen](#seen)

- [send_activity](#send_activity)

- [unban_member](#unban_member)

- [unpin](#unpin)

---

## متدهای Static

<a name="ban_member"></a>
### `ban_member(self, object_guid: str = None, user_guid: str = None)`

**نوع متد:** Static

```python
ban_member(self, object_guid: str = None, user_guid: str = None)
```

Ban a member.

Args:
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
    - user_guid (str, optional): User GUID. Defaults to None.

Returns:
    - dict: Result of the ban operation.

---
<a name="block"></a>
### `block(self, user_guid: str = None)`

**نوع متد:** Static

```python
block(self, user_guid: str = None)
```

Block a user.

Args:
    - user_guid (str, optional): User GUID. Defaults to update.object_guid.

Returns:
    - dict: Result of the admin check operation.

---
<a name="copy"></a>
### `copy(self, to_object_guid: str, from_object_guid: str = None, message_ids=None, *args, **kwargs)`

**نوع متد:** Static

```python
copy(self, to_object_guid: str, from_object_guid: str = None, message_ids=None, *args, **kwargs)
```

Copy messages to another object.

Args:
    - to_object_guid (str): To object guid.
    - from_object_guid (str, optional): From object guid. Defaults to update.object_guid.
    - message_ids (Union[str, int, List[str]], optional): Message ids. Defaults to update.message_id.

---
<a name="delete"></a>
### `delete(self)`

**نوع متد:** Static

```python
delete(self)
```

Delete message.

Returns:
    - dict: Result of the message deletion operation.

---
<a name="delete_messages"></a>
### `delete_messages(self, object_guid: str = None, message_ids: list = None)`

**نوع متد:** Static

```python
delete_messages(self, object_guid: str = None, message_ids: list = None)
```

Delete messages.

Args:
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
    - message_ids (list, optional): Custom message IDs. Defaults to update.message_id.

Returns:
    - dict: Result of the message deletion operation.

---
<a name="download"></a>
### `download(self, file_inline=None, save_as=None, *args, **kwargs)`

**نوع متد:** Static

```python
download(self, file_inline=None, save_as=None, *args, **kwargs)
```

Download a file.

Args:
- file_inline (dict, optional): File information. Defaults to update.file_inline.
- save_as (str, optional): The path to save the downloaded file. If None, the file will not be saved.
- chunk_size (int, optional): The size of each chunk to download.
- callback (callable, optional): A callback function to monitor the download progress.
- *args, **kwargs: Additional parameters to pass to the download method.

Returns:
- bytes: The binary data of the downloaded file.

Raises:
- aiofiles.errors.OSFError: If there is an issue with file I/O (when saving the file).

---
<a name="edit"></a>
### `edit(self, text: str, object_guid: str = None, message_id: str = None, *args, **kwargs)`

**نوع متد:** Static

```python
edit(self, text: str, object_guid: str = None, message_id: str = None, *args, **kwargs)
```

Edit a message.

Args:
    - text (str): The new message text.
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid if not provided.
    - message_id (str, optional): Custom message ID. Defaults to update.message_id if not provided.

Returns:
    - dict: Result of the edit operation.

---
<a name="find_keys"></a>
### `find_keys(self, keys, original_update=None, *args, **kwargs)`

**نوع متد:** Static

```python
find_keys(self, keys, original_update=None, *args, **kwargs)
```

توضیحی موجود نیست.

---
<a name="forward"></a>
### `forward(self, to_object_guid: str)`

**نوع متد:** Static

```python
forward(self, to_object_guid: str)
```

Forward message.

Args:
    - to_object_guid (str): Destination object GUID.

Returns:
    - dict: Result of the forward operation.

---
<a name="forwards"></a>
### `forwards(self, to_object_guid: str, from_object_guid: str = None, message_ids=None)`

**نوع متد:** Static

```python
forwards(self, to_object_guid: str, from_object_guid: str = None, message_ids=None)
```

Forward messages.

Args:
    - to_object_guid (str): Destination object GUID.
    - from_object_guid (str, optional): Source object GUID. Defaults to update.object_guid.
    - message_ids (Union[str, int, List[str]], optional): Message IDs to forward. Defaults to update.message_id.

Returns:
    - dict: Result of the forward operation.

---
<a name="get_author"></a>
### `get_author(self, author_guid: str = None, *args, **kwargs)`

**نوع متد:** Static

```python
get_author(self, author_guid: str = None, *args, **kwargs)
```

Get user or author information.

Args:
    - author_guid (str, optional): Custom author GUID. Defaults to update.author_guid.

Returns:
    - dict: User or author information.

---
<a name="get_messages"></a>
### `get_messages(self, object_guid: str = None, message_ids=None)`

**نوع متد:** Static

```python
get_messages(self, object_guid: str = None, message_ids=None)
```

Get messages.

Args:
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
    - message_ids (Union[str, int, List[str]], optional): Message IDs. Defaults to update.message_id.

Returns:
    - dict: Retrieved messages.

---
<a name="get_object"></a>
### `get_object(self, object_guid: str = None)`

**نوع متد:** Static

```python
get_object(self, object_guid: str = None)
```

Get object information.

Args:
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.

Returns:
    - dict: Object information.

---
<a name="get_reply_author"></a>
### `get_reply_author(self, object_guid: str = None, reply_message_id: str = None)`

**نوع متد:** Static

```python
get_reply_author(self, object_guid: str = None, reply_message_id: str = None)
```

توضیحی موجود نیست.

---
<a name="get_reply_message"></a>
### `get_reply_message(self, object_guid: str = None, reply_message_id: str = None)`

**نوع متد:** Static

```python
get_reply_message(self, object_guid: str = None, reply_message_id: str = None)
```

توضیحی موجود نیست.

---
<a name="guid_type"></a>
### `guid_type(self, object_guid: str = None)`

**نوع متد:** Static

```python
guid_type(self, object_guid: str = None)
```

Determine the type of the object based on its GUID.

Args:
    - object_guid (str): The GUID of the object.

Returns:
    - str: The type of the object ('Channel', 'Group', or 'User').

---
<a name="is_admin"></a>
### `is_admin(self, object_guid: str = None, user_guid: str = None)`

**نوع متد:** Static

```python
is_admin(self, object_guid: str = None, user_guid: str = None)
```

Check if a user is an admin.

Args:
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
    - user_guid (str, optional): User GUID. Defaults to update.object_guid.

Returns:
    - dict: Result of the admin check operation.

---
<a name="jsonify"></a>
### `jsonify(self, indent=None) -> str`

**نوع متد:** Static

```python
jsonify(self, indent=None) -> str
```

توضیحی موجود نیست.

---
<a name="pin"></a>
### `pin(self, object_guid: str = None, message_id: str = None, action: str = 'Pin')`

**نوع متد:** Static

```python
pin(self, object_guid: str = None, message_id: str = None, action: str = 'Pin')
```

Pin a message.

Args:
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid if not provided.
    - message_id (str, optional): Custom message ID. Defaults to update.message_id if not provided.
    - action (str, optional): Pin or unpin action. Defaults to 'Pin'.

Returns:
    - BaseResults: Result of the pin or unpin operation.

---
<a name="reaction"></a>
### `reaction(self, reaction_id: int, object_guid: str = None, message_id: str = None)`

**نوع متد:** Static

```python
reaction(self, reaction_id: int, object_guid: str = None, message_id: str = None)
```

Add a reaction to a message.

Args:
    - reaction_id (int): Reaction ID.
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
    - message_id (str, optional): Custom message ID. Defaults to update.message_id.

Returns:
    - dict: Result of the reaction operation.

---
<a name="reply"></a>
### `reply(self, text: str = None, object_guid: str = None, reply_to_message_id: str = None, file_inline=None, auto_delete: int = None, *args, **kwargs)`

**نوع متد:** Static

```python
reply(self, text: str = None, object_guid: str = None, reply_to_message_id: str = None, file_inline=None, auto_delete: int = None, *args, **kwargs)
```

Reply to a message.

Args:
    - text (str, optional): Text content of the reply. Defaults to None.
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
    - reply_to_message_id (str, optional): Reply to message ID. Defaults to None.
    - file_inline (Union[pathlib.Path, bytes], optional): File to send with the reply. Defaults to None.
    - auto_delete (int, optional): Auto-delete timer for the message. Defaults to None.
    - *args, **kwargs: Additional arguments.

Returns:
    - dict: Result of the reply operation.

---
<a name="reply_document"></a>
### `reply_document(self, document: Union[str, bytes, pathlib._local.Path], caption: str = None, auto_delete: int = None, object_guid: str = None, reply_to_message_id: str = None, *args, **kwargs)`

**نوع متد:** Static

```python
reply_document(self, document: Union[str, bytes, pathlib._local.Path], caption: str = None, auto_delete: int = None, object_guid: str = None, reply_to_message_id: str = None, *args, **kwargs)
```

Reply with a document.

Args:
    - document (Union[str, bytes, Path]): Document to reply with.
    - caption (str, optional): Caption for the document. Defaults to None.
    - auto_delete (int, optional): Auto-delete timer for the message. Defaults to None.
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
    - reply_to_message_id (str, optional): Reply to message ID. Defaults to None.
    - *args, **kwargs: Additional arguments.

Returns:
    - dict: Result of the reply operation.

---
<a name="reply_gif"></a>
### `reply_gif(self, gif: Union[str, bytes, pathlib._local.Path], caption: str = None, auto_delete: int = None, object_guid: str = None, reply_to_message_id: str = None, *args, **kwargs)`

**نوع متد:** Static

```python
reply_gif(self, gif: Union[str, bytes, pathlib._local.Path], caption: str = None, auto_delete: int = None, object_guid: str = None, reply_to_message_id: str = None, *args, **kwargs)
```

Reply with a gif.

Args:
    - gif (Union[str, bytes, Path]): Gif to reply with.
    - caption (str, optional): Caption for the Gif. Defaults to None.
    - auto_delete (int, optional): Auto-delete timer for the message. Defaults to None.
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
    - reply_to_message_id (str, optional): Reply to message ID. Defaults to None.
    - *args, **kwargs: Additional arguments.

Returns:
    - dict: Result of the reply operation.

---
<a name="reply_music"></a>
### `reply_music(self, music: Union[str, bytes, pathlib._local.Path], caption: str = None, auto_delete: int = None, object_guid: str = None, reply_to_message_id: str = None, *args, **kwargs)`

**نوع متد:** Static

```python
reply_music(self, music: Union[str, bytes, pathlib._local.Path], caption: str = None, auto_delete: int = None, object_guid: str = None, reply_to_message_id: str = None, *args, **kwargs)
```

Reply with a music.

Args:
    - music (Union[str, bytes, Path]): Music to reply with.
    - caption (str, optional): Caption for the Music. Defaults to None.
    - auto_delete (int, optional): Auto-delete timer for the message. Defaults to None.
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
    - reply_to_message_id (str, optional): Reply to message ID. Defaults to None.
    - *args, **kwargs: Additional arguments.

Returns:
    - dict: Result of the reply operation.

---
<a name="reply_photo"></a>
### `reply_photo(self, photo: Union[str, bytes, pathlib._local.Path], caption: str = None, auto_delete: int = None, object_guid: str = None, reply_to_message_id: str = None, *args, **kwargs)`

**نوع متد:** Static

```python
reply_photo(self, photo: Union[str, bytes, pathlib._local.Path], caption: str = None, auto_delete: int = None, object_guid: str = None, reply_to_message_id: str = None, *args, **kwargs)
```

Reply with a photo.

Args:
    - photo (Union[str, bytes, Path]): Photo to reply with.
    - caption (str, optional): Caption for the photo. Defaults to None.
    - auto_delete (int, optional): Auto-delete timer for the message. Defaults to None.
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
    - reply_to_message_id (str, optional): Reply to message ID. Defaults to None.
    - *args, **kwargs: Additional arguments.

Returns:
    - dict: Result of the reply operation.

---
<a name="reply_video"></a>
### `reply_video(self, video: Union[str, bytes, pathlib._local.Path], caption: str = None, auto_delete: int = None, object_guid: str = None, reply_to_message_id: str = None, *args, **kwargs)`

**نوع متد:** Static

```python
reply_video(self, video: Union[str, bytes, pathlib._local.Path], caption: str = None, auto_delete: int = None, object_guid: str = None, reply_to_message_id: str = None, *args, **kwargs)
```

Reply with a video.

Args:
    - video (Union[str, bytes, Path]): Video to reply with.
    - caption (str, optional): Caption for the Video. Defaults to None.
    - auto_delete (int, optional): Auto-delete timer for the message. Defaults to None.
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
    - reply_to_message_id (str, optional): Reply to message ID. Defaults to None.
    - *args, **kwargs: Additional arguments.

Returns:
    - dict: Result of the reply operation.

---
<a name="reply_video_message"></a>
### `reply_video_message(self, video: Union[str, bytes, pathlib._local.Path], caption: str = None, auto_delete: int = None, object_guid: str = None, reply_to_message_id: str = None, *args, **kwargs)`

**نوع متد:** Static

```python
reply_video_message(self, video: Union[str, bytes, pathlib._local.Path], caption: str = None, auto_delete: int = None, object_guid: str = None, reply_to_message_id: str = None, *args, **kwargs)
```

Reply with a video.

Args:
    - video (Union[str, bytes, Path]): VideoMessage to reply with.
    - caption (str, optional): Caption for the VideoMessage. Defaults to None.
    - auto_delete (int, optional): Auto-delete timer for the message. Defaults to None.
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
    - reply_to_message_id (str, optional): Reply to message ID. Defaults to None.
    - *args, **kwargs: Additional arguments.

Returns:
    - dict: Result of the reply operation.

---
<a name="reply_voice"></a>
### `reply_voice(self, voice: Union[str, bytes, pathlib._local.Path], caption: str = None, auto_delete: int = None, object_guid: str = None, reply_to_message_id: str = None, *args, **kwargs)`

**نوع متد:** Static

```python
reply_voice(self, voice: Union[str, bytes, pathlib._local.Path], caption: str = None, auto_delete: int = None, object_guid: str = None, reply_to_message_id: str = None, *args, **kwargs)
```

Reply with a voice.

Args:
    - voice (Union[str, bytes, Path]): Voice to reply with.
    - caption (str, optional): Caption for the Voice. Defaults to None.
    - auto_delete (int, optional): Auto-delete timer for the message. Defaults to None.
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
    - reply_to_message_id (str, optional): Reply to message ID. Defaults to None.
    - *args, **kwargs: Additional arguments.

Returns:
    - dict: Result of the reply operation.

---
<a name="seen"></a>
### `seen(self, seen_list: dict = None)`

**نوع متد:** Static

```python
seen(self, seen_list: dict = None)
```

Mark chats as seen.

Args:
    - seen_list (dict, optional): Dictionary containing object GUIDs and corresponding message IDs.
        Defaults to {update.object_guid: update.message_id} if not provided.

Returns:
    - dict: Result of the operation.

---
<a name="send_activity"></a>
### `send_activity(self, activity: Literal['Typing', 'Uploading', 'Recording'] = 'Typing', object_guid: str = None)`

**نوع متد:** Static

```python
send_activity(self, activity: Literal['Typing', 'Uploading', 'Recording'] = 'Typing', object_guid: str = None)
```

Send chat activity.

Args:
    - activity (Literal['Typing', 'Uploading', 'Recording'], optional): Chat activity type. Defaults to 'Typing'.
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.

Returns:
    - dict: Result of the activity sending operation.

---
<a name="unban_member"></a>
### `unban_member(self, object_guid: str = None, user_guid: str = None)`

**نوع متد:** Static

```python
unban_member(self, object_guid: str = None, user_guid: str = None)
```

Unban a member.

Args:
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
    - user_guid (str, optional): User GUID. Defaults to None.

Returns:
    - dict: Result of the unban operation.

---
<a name="unpin"></a>
### `unpin(self, object_guid: str = None, message_id: str = None)`

**نوع متد:** Static

```python
unpin(self, object_guid: str = None, message_id: str = None)
```

Unpin a message.

Args:
    - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid if not provided.
    - message_id (str, optional): Custom message ID. Defaults to update.message_id if not provided.
    - action (str, optional): Pin or unpin action. Defaults to 'Pin'.

Returns:
    - BaseResults: Result of the pin or unpin operation.

---

*مستندات به‌صورت خودکار تولید شده‌اند.*