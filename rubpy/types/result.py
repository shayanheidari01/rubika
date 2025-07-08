from json import dumps
from typing import Literal, Union, Type
from pathlib import Path
import rubpy
import warnings


class Update:
    command: Type[Union[list, None]]

    def __str__(self) -> str:
        return self.jsonify(indent=2)

    def __getattr__(self, name):
        return self.find_keys(keys=name)

    def __setitem__(self, key, value):
        self.original_update[key] = value

    def __getitem__(self, key):
        return self.original_update[key]

    def __lts__(self, update: list, *args, **kwargs):
        for index, element in enumerate(update):
            if isinstance(element, list):
                update[index] = self.__lts__(update=element)
            elif isinstance(element, dict):
                update[index] = Update(update=element)
            else:
                update[index] = element
        return update

    def __init__(self, update: dict, *args, **kwargs) -> None:
        self.client: "rubpy.Client" = update.get('client')
        self.original_update = update

    def jsonify(self, indent=None) -> str:
        result = self.original_update
        result['original_update'] = 'dict{...}'
        return dumps(result, indent=indent, ensure_ascii=False, default=lambda value: str(value))

    def find_keys(self, keys, original_update=None, *args, **kwargs):
        if original_update is None:
            original_update = self.original_update

        if not isinstance(keys, list):
            keys = [keys]

        if isinstance(original_update, dict):
            for key in keys:
                try:
                    update = original_update[key]
                    if isinstance(update, dict):
                        update = Update(update=update)
                    elif isinstance(update, list):
                        update = self.__lts__(update=update)
                    return update
                except KeyError:
                    pass
            original_update = original_update.values()

        for value in original_update:
            if isinstance(value, (dict, list)):
                try:
                    return self.find_keys(keys=keys, original_update=value)
                except AttributeError:
                    return None

        return None

    @property
    def to_dict(self) -> dict:
        "Return the update as dict"
        return self.original_update

    @property
    def is_me(self):
        return self.message.is_mine

    @property
    def status(self):
        return self.find_keys('status')

    @property
    def action(self):
        return self.find_keys('action')

    @property
    def is_edited(self) -> bool:
        return self.message.is_edited

    @property
    def type(self):
        return self.find_keys(keys=['type', 'author_type'])

    @property
    def title(self) -> str:
        return self.find_keys('title')

    @property
    def is_forward(self) -> bool:
        return self.find_keys('forwarded_from')

    @property
    def forward_type_from(self):
        return self.find_keys('type_from')

    @property
    def is_event(self) -> bool:
        return self.find_keys('event_data')

    @property
    def file_inline(self):
        return self.find_keys('file_inline')

    @property
    def text(self) -> str:
        return self.find_keys(keys='text')

    @property
    def raw_text(self):
        warnings.warn('The `raw_text` property will be removed soon, please use `text` instead')
        return self.find_keys(keys='text')

    @property
    def message_id(self):
        return self.find_keys(keys=['message_id', 'pinned_message_id'])

    @property
    def reply_message_id(self):
        return self.find_keys(keys='reply_to_message_id')

    @property
    def is_group(self):
        return self.type == 'Group'

    @property
    def is_channel(self):
        return self.type == 'Channel'

    @property
    def is_private(self):
        return self.type == 'User'

    @property
    def object_guid(self):
        return self.find_keys(keys=['group_guid', 'object_guid', 'channel_guid'])

    @property
    def author_guid(self):
        return self.author_object_guid

    @property
    def is_text(self):
        return self.message.type == 'Text'

    def guid_type(self, object_guid: str = None):
        """
        Determine the type of the object based on its GUID.

        Args:
            - object_guid (str): The GUID of the object.

        Returns:
            - str: The type of the object ('Channel', 'Group', or 'User').
        """
        if object_guid is None:
            object_guid = self.object_guid

        if object_guid.startswith('c0'):
            return 'Channel'
        elif object_guid.startswith('g0'):
            return 'Group'
        else:
            return 'User'

    # async methods

    async def pin(self, object_guid: str = None, message_id: str = None, action: str = 'Pin'):
        """
        Pin a message.

        Args:
            - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid if not provided.
            - message_id (str, optional): Custom message ID. Defaults to update.message_id if not provided.
            - action (str, optional): Pin or unpin action. Defaults to 'Pin'.

        Returns:
            - BaseResults: Result of the pin or unpin operation.
        """
        if object_guid is None:
            object_guid = self.object_guid

        if message_id is None:
            message_id = self.message_id

        return await self.client.set_pin_message(object_guid, message_id, action)

    async def unpin(self, object_guid: str = None, message_id: str = None):
        """
        Unpin a message.

        Args:
            - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid if not provided.
            - message_id (str, optional): Custom message ID. Defaults to update.message_id if not provided.
            - action (str, optional): Pin or unpin action. Defaults to 'Pin'.

        Returns:
            - BaseResults: Result of the pin or unpin operation.
        """
        if object_guid is None:
            object_guid = self.object_guid

        if message_id is None:
            message_id = self.message_id

        return await self.client.set_pin_message(object_guid, message_id, 'Unpin')

    async def edit(self, text: str, object_guid: str = None, message_id: str = None, *args, **kwargs):
        """
        Edit a message.

        Args:
            - text (str): The new message text.
            - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid if not provided.
            - message_id (str, optional): Custom message ID. Defaults to update.message_id if not provided.

        Returns:
            - dict: Result of the edit operation.
        """
        if object_guid is None:
            object_guid = self.object_guid

        if message_id is None:
            message_id = self.message_id

        return await self.client.edit_message(object_guid, message_id, text)

    async def copy(self, to_object_guid: str, from_object_guid: str = None, message_ids=None, *args, **kwargs):
        """
        Copy messages to another object.

        Args:
            - to_object_guid (str): To object guid.
            - from_object_guid (str, optional): From object guid. Defaults to update.object_guid.
            - message_ids (Union[str, int, List[str]], optional): Message ids. Defaults to update.message_id.
        """
        if from_object_guid is None:
            from_object_guid = self.object_guid

        if message_ids is None:
            message_ids = self.message_id

        result = await self.get_messages(from_object_guid, message_ids)
        messages = []

        if result.messages:
            for message in result.messages:
                file_inline = message.file_inline
                sticker = message.sticker
                text = message.text

                if sticker:
                    result = await self.client.send_message(to_object_guid, sticker=sticker.to_dict)
                    messages.append(result)
                    continue
                elif file_inline:
                    kwargs.update(file_inline.to_dict)
                    if file_inline.type not in ['Gif', 'Sticker']:
                        file_inline = await self.download(file_inline)
                        messages.append(await self.client.send_message(
                            object_guid=to_object_guid,
                            text=text,
                            file_inline=file_inline, *args, **kwargs))
                        continue

                result = await self.client.send_message(to_object_guid, text, file_inline=file_inline, *args, **kwargs)
                messages.append(result)

        return Update({'status': 'OK', 'messages': messages})

    async def seen(self, seen_list: dict = None):
        """
        Mark chats as seen.

        Args:
            - seen_list (dict, optional): Dictionary containing object GUIDs and corresponding message IDs.
                Defaults to {update.object_guid: update.message_id} if not provided.

        Returns:
            - dict: Result of the operation.
        """
        if seen_list is None:
            seen_list = {self.object_guid: self.message_id}
        return await self.client.seen_chats(seen_list)

    async def reply(self, text: str = None, object_guid: str = None, reply_to_message_id: str = None,
                file_inline=None, auto_delete: int = None, *args, **kwargs):
        """
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
        """
        if object_guid is None:
            object_guid = self.object_guid

        if reply_to_message_id is None:
            reply_to_message_id = self.message_id

        return await self.client.send_message(object_guid, text, reply_to_message_id=reply_to_message_id,
                                            file_inline=file_inline,
                                            auto_delete=auto_delete,
                                            *args, **kwargs)

    async def reply_document(self, document: Union[str, bytes, Path], caption: str = None,
                            auto_delete: int = None, object_guid: str = None,
                            reply_to_message_id: str = None, *args, **kwargs):
        """
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
        """
        return await self.reply(text=caption, object_guid=object_guid, reply_to_message_id=reply_to_message_id,
                                file_inline=document, type='File', auto_delete=auto_delete, *args, **kwargs)

    async def reply_photo(self, photo: Union[str, bytes, Path], caption: str = None,
                        auto_delete: int = None, object_guid: str = None,
                        reply_to_message_id: str = None, *args, **kwargs):
        """
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
        """
        return await self.reply(text=caption, object_guid=object_guid, reply_to_message_id=reply_to_message_id,
                                file_inline=photo, type='Image', auto_delete=auto_delete, *args, **kwargs)

    async def reply_video(self, video: Union[str, bytes, Path], caption: str = None,
                           auto_delete: int = None, object_guid: str = None,
                           reply_to_message_id: str = None, *args, **kwargs):
        """
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
        """
        return await self.reply(text=caption, object_guid=object_guid, reply_to_message_id=reply_to_message_id,
                                 file_inline=video, type='Video', auto_delete=auto_delete, *args, **kwargs)

    async def reply_music(self, music: Union[str, bytes, Path], caption: str = None,
                           auto_delete: int = None, object_guid: str = None,
                           reply_to_message_id: str = None, *args, **kwargs):
        """
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
        """
        return await self.reply(text=caption, object_guid=object_guid, reply_to_message_id=reply_to_message_id,
                                 file_inline=music, type='Music', auto_delete=auto_delete, *args, **kwargs)

    async def reply_voice(self, voice: Union[str, bytes, Path], caption: str = None,
                           auto_delete: int = None, object_guid: str = None,
                           reply_to_message_id: str = None, *args, **kwargs):
        """
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
        """
        return await self.reply(text=caption, object_guid=object_guid, reply_to_message_id=reply_to_message_id,
                                 file_inline=voice, type='Voice', auto_delete=auto_delete, *args, **kwargs)

    async def reply_gif(self, gif: Union[str, bytes, Path], caption: str = None,
                         auto_delete: int = None, object_guid: str = None,
                         reply_to_message_id: str = None, *args, **kwargs):
        """
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
        """
        return await self.reply(text=caption, object_guid=object_guid, reply_to_message_id=reply_to_message_id,
                                 file_inline=gif, type='Gif', auto_delete=auto_delete, *args, **kwargs)

    async def reply_video_message(self, video: Union[str, bytes, Path], caption: str = None,
                                   auto_delete: int = None, object_guid: str = None,
                                   reply_to_message_id: str = None, *args, **kwargs):
        """
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
        """
        return await self.reply(text=caption, object_guid=object_guid, reply_to_message_id=reply_to_message_id,
                                 file_inline=video, type='VideoMessage', auto_delete=auto_delete, *args, **kwargs)

    async def forward(self, to_object_guid: str):
        """
        Forward message.

        Args:
            - to_object_guid (str): Destination object GUID.

        Returns:
            - dict: Result of the forward operation.
        """
        return await self.client.forward_messages(
            from_object_guid=self.object_guid,
            to_object_guid=to_object_guid,
            message_ids=[self.message_id],
        )

    async def forwards(self, to_object_guid: str, from_object_guid: str = None, message_ids=None):
        """
        Forward messages.

        Args:
            - to_object_guid (str): Destination object GUID.
            - from_object_guid (str, optional): Source object GUID. Defaults to update.object_guid.
            - message_ids (Union[str, int, List[str]], optional): Message IDs to forward. Defaults to update.message_id.

        Returns:
            - dict: Result of the forward operation.
        """
        if from_object_guid is None:
            from_object_guid = self.object_guid

        if message_ids is None:
            message_ids = [self.message_id]

        return await self.client.forward_messages(
            from_object_guid=from_object_guid,
            to_object_guid=to_object_guid,
            message_ids=message_ids,
        )

    async def download(self, file_inline=None, save_as=None, *args, **kwargs):
        """
        Download a file.

        Args:
            - file_inline (dict, optional): File information. Defaults to None.
            - file (str, optional): Path to save the downloaded file. Defaults to None.
            - *args, **kwargs: Additional arguments.

        Returns:
            - bytes: Downloaded file content.
        """
        if isinstance(file_inline, dict):
            file_inline = Update(file_inline)

        return await self.client.download(file_inline or self.file_inline, save_as=save_as, *args, **kwargs)

    async def get_author(self, author_guid: str = None, *args, **kwargs):
        """
        Get user or author information.

        Args:
            - author_guid (str, optional): Custom author GUID. Defaults to update.author_guid.

        Returns:
            - dict: User or author information.
        """
        if author_guid is None:
            author_guid = self.author_guid

        return await self.get_object(object_guid=author_guid, *args, **kwargs)

    async def get_object(self, object_guid: str = None):
        """
        Get object information.

        Args:
            - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.

        Returns:
            - dict: Object information.
        """
        if object_guid is None:
            object_guid = self.object_guid

        if self.guid_type(object_guid) == 'User':
            return await self.client.get_user_info(object_guid)
        elif self.guid_type(object_guid) == 'Group':
            return await self.client.get_group_info(object_guid)
        elif self.guid_type(object_guid) == 'Channel':
            return await self.client.get_channel_info(object_guid)

    async def get_messages(self, object_guid: str = None, message_ids=None):
        """
        Get messages.

        Args:
            - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
            - message_ids (Union[str, int, List[str]], optional): Message IDs. Defaults to update.message_id.

        Returns:
            - dict: Retrieved messages.
        """
        if object_guid is None:
            object_guid = self.object_guid

        if message_ids is None:
            message_ids = self.message_id

        return await self.client.get_messages_by_id(
            object_guid=object_guid,
            message_ids=message_ids,
        )

    async def delete(self):
        """
        Delete message.

        Returns:
            - dict: Result of the message deletion operation.
        """
        return await self.client.delete_messages(
            object_guid=self.object_guid,
            message_ids=[self.message_id],
        )

    async def delete_messages(self, object_guid: str = None, message_ids: list = None):
        """
        Delete messages.

        Args:
            - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
            - message_ids (list, optional): Custom message IDs. Defaults to update.message_id.

        Returns:
            - dict: Result of the message deletion operation.
        """
        if object_guid is None:
            object_guid = self.object_guid

        if message_ids is None:
            message_ids = self.message_id

        return await self.client.delete_messages(
            object_guid=object_guid,
            message_ids=message_ids,
        )

    async def reaction(self, reaction_id: int, object_guid: str = None, message_id: str = None):
        """
        Add a reaction to a message.

        Args:
            - reaction_id (int): Reaction ID.
            - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
            - message_id (str, optional): Custom message ID. Defaults to update.message_id.

        Returns:
            - dict: Result of the reaction operation.
        """
        if object_guid is None:
            object_guid = self.object_guid

        if message_id is None:
            message_id = self.message_id

        return await self.client.action_on_message_reaction(
            object_guid=object_guid,
            message_id=message_id,
            action='Add',
            reaction_id=reaction_id,
        )

    async def ban_member(self, object_guid: str = None, user_guid: str = None):
        """
        Ban a member.

        Args:
            - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
            - user_guid (str, optional): User GUID. Defaults to None.

        Returns:
            - dict: Result of the ban operation.
        """
        if object_guid is None:
            object_guid = self.object_guid
        if user_guid is None:
            user_guid = self.author_guid

        if object_guid.startswith('g0'):
            return await self.client.ban_group_member(object_guid, user_guid)
        elif object_guid.startswith('c0'):
            return await self.client.ban_channel_member(object_guid, user_guid)

    async def unban_member(self, object_guid: str = None, user_guid: str = None):
        """
        Unban a member.

        Args:
            - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
            - user_guid (str, optional): User GUID. Defaults to None.

        Returns:
            - dict: Result of the unban operation.
        """
        if object_guid is None:
            object_guid = self.object_guid
        if user_guid is None:
            user_guid = self.author_guid

        if object_guid.startswith('g0'):
            return await self.client.ban_group_member(object_guid, user_guid, 'Unset')
        elif object_guid.startswith('c0'):
            return await self.client.ban_channel_member(object_guid, user_guid, 'Unset')

    async def send_activity(self, activity: Literal['Typing', 'Uploading', 'Recording'] = 'Typing', object_guid: str = None):
        """
        Send chat activity.

        Args:
            - activity (Literal['Typing', 'Uploading', 'Recording'], optional): Chat activity type. Defaults to 'Typing'.
            - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.

        Returns:
            - dict: Result of the activity sending operation.
        """
        if object_guid is None:
            object_guid = self.object_guid

        return await self.client.send_chat_activity(
            object_guid=object_guid,
            activity=activity,
        )

    async def is_admin(self, object_guid: str = None, user_guid: str = None):
        """
        Check if a user is an admin.

        Args:
            - object_guid (str, optional): Custom object GUID. Defaults to update.object_guid.
            - user_guid (str, optional): User GUID. Defaults to update.object_guid.

        Returns:
            - dict: Result of the admin check operation.
        """
        if object_guid is None:
            object_guid = self.object_guid

        if user_guid is None:
            user_guid = self.author_guid

        return await self.client.user_is_admin(
            object_guid=object_guid,
            user_guid=user_guid,
        )

    async def block(self, user_guid: str = None):
        """
        Block a user.

        Args:
            - user_guid (str, optional): User GUID. Defaults to update.object_guid.

        Returns:
            - dict: Result of the admin check operation.
        """
        if user_guid is None:
            user_guid = self.object_guid if self.guid_type(user_guid) == 'User' else self.author_guid

        return await self.client.set_block_user(user_guid=user_guid)

    async def get_reply_author(self, object_guid: str = None, reply_message_id: str = None):
        result = await self.client.get_messages_by_id(
            object_guid or self.object_guid,
            message_ids=reply_message_id or self.reply_message_id)
        return await self.client.get_info(result.messages[0].author_object_guid)

    async def get_reply_message(self, object_guid: str = None, reply_message_id: str = None):
        result = await self.client.get_messages_by_id(
            object_guid or self.object_guid,
            message_ids=reply_message_id or self.reply_message_id)
        return result.messages[0]