from json import dumps
from typing import Literal, Union, Type
from pathlib import Path
import rubpy
thumbnail = None


class SocketResults:
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
                update[index] = SocketResults(update=element)
            else:
                update[index] = element
        return update

    def __init__(self, update: dict, *args, **kwargs) -> None:
        self.client: "rubpy.Client" = update.get('client')
        self.original_update = update

    def to_dict(self):
        return self.original_update

    def jsonify(self, indent=None, *args, **kwargs) -> str:
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
                        update = SocketResults(update=update)
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
    def type(self):
        try:
            return self.find_keys(keys=['type', 'author_type'])
        except AttributeError:
            pass

    @property
    def raw_text(self):
        try:
            return self.find_keys(keys='text')
        except AttributeError:
            pass

    @property
    def message_id(self):
        try:
            return self.find_keys(keys=['message_id', 'pinned_message_id'])
        except AttributeError:
            pass

    @property
    def reply_message_id(self):
        try:
            return self.find_keys(keys='reply_to_message_id')
        except AttributeError:
            pass

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
    def text(self):
        return self.message.type == 'Text'

    def guid_type(self, object_guid: str):
        if object_guid.startswith('c0'):
            return 'Channel'
        elif object_guid.startswith('g0'):
            return 'Group'
        else:
            return 'User'

    # async methods

    async def pin(self, object_guid: str = None, message_id: str = None, action: str = 'Pin'):
        """_pin_
        Args:
            object_guid (str, optional):
                _custom object guid_. Defaults to update.object_guid.
            message_id (str, optional):
                _custom message id_. Defaults to update.message_id.
            action (bool, optional):
                _pin or unpin_. Defaults to methods.messages.Pin. (
                    methods.messages.Pin,
                    methods.messages.Unpin
                )
        Returns:
            BaseResults: result
        """
        if object_guid is None:
            object_guid = self.object_guid

        if message_id is None:
            message_id = self.message_id

        return await self.client.set_pin_message(object_guid, message_id, action)

    async def edit(self, text: str, object_guid: str = None, message_id: str = None, *args, **kwargs):
        """_edit_
        Args:
            text (str):
                _message text_
            object_guid (str, optional):
                _custom objec guid_. Defaults to update.object_guid.
            message_id (str, optional):
                _custom message id_. Defaults to update.message_id.
        """
        if object_guid is None:
            object_guid = self.object_guid

        if message_id is None:
            message_id = self.message_id

        return await self.client.edit_message(object_guid, message_id, text)

    async def copy(self, to_object_guid: str, from_object_guid: str = None, message_ids=None, *args, **kwargs):
        """_copy_
        Args:
            to_object_guid (str):
                _to object guid_.
            from_object_guid (str, optional):
                _from object guid_. Defaults to update.object_guid.
            message_ids (typing.Union[str, int, typing.List[str]], optional):
                _message ids_. Defaults to update.message_id.
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
                    result = await self.client.send_message(to_object_guid, sticker=sticker.to_dict())
                    messages.append(result)
                    continue
                elif file_inline:
                    kwargs.update(file_inline.to_dict())
                    if file_inline.type not in ['Gif', 'Sticker']:
                        file_inline = await self.download(file_inline)
                        messages.append(await self.client.send_message(
                            object_guid=to_object_guid,
                            text=text,
                            file_inline=file_inline, *args, **kwargs))
                        continue

                result = await self.client.send_message(to_object_guid, text, file_inline=file_inline, *args, **kwargs)
                messages.append(result)

        return SocketResults({'status': 'OK', 'messages': messages})

    async def seen(self, seen_list: dict = None):
        """_seen_
        Args:
            seen_list (dict, optional):
                _description_. Defaults to {update.object_guid: update.message_id}.
        """
        if seen_list is None:
            seen_list = {self.object_guid: self.message_id}
        return await self.client.seen_chats(seen_list)

    async def reply(self, text: str = None, object_guid: str = None, reply_to_message_id: str = None,
                    file_inline=None, auto_delete: int = None, *args, **kwargs):
        """_reply_
        Args:
            message (Any, optional):
                _message or cation or sticker_ . Defaults to None.
            object_guid (str):
                _object guid_ . Defaults to update.object_guid
            reply_to_message_id (str, optional):
                _reply to message id_. Defaults to None.
            file_inline (typing.Union[pathlib.Path, bytes], optional):
                _file_. Defaults to None.
            type ('Image', 'Video', 'File', 'Voice', 'Music')
                _type_. Defaults to 'File'.
            thumb (bool, optional):
                if value is "True",
                the lib will try to build the thumb ( require cv2 )
                if value is thumbnail.Thumbnail, to set custom
                Defaults to True.
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
        return await self.reply(text=caption, object_guid=object_guid, reply_to_message_id=reply_to_message_id,
                                 file_inline=document, type='File', auto_delete=auto_delete, *args, **kwargs)

    async def reply_photo(self, photo: Union[str, bytes, Path], caption: str = None,
                           auto_delete: int = None, object_guid: str = None,
                           reply_to_message_id: str = None, *args, **kwargs):
        return await self.reply(text=caption, object_guid=object_guid, reply_to_message_id=reply_to_message_id,
                                 file_inline=photo, type='Image', auto_delete=auto_delete, *args, **kwargs)

    async def reply_video(self, video: Union[str, bytes, Path], caption: str = None,
                           auto_delete: int = None, object_guid: str = None,
                           reply_to_message_id: str = None, *args, **kwargs):
        return await self.reply(text=caption, object_guid=object_guid, reply_to_message_id=reply_to_message_id,
                                 file_inline=video, type='Video', auto_delete=auto_delete, *args, **kwargs)

    async def reply_music(self, video: Union[str, bytes, Path], caption: str = None,
                           auto_delete: int = None, object_guid: str = None,
                           reply_to_message_id: str = None, *args, **kwargs):
        return await self.reply(text=caption, object_guid=object_guid, reply_to_message_id=reply_to_message_id,
                                 file_inline=video, type='Music', auto_delete=auto_delete, *args, **kwargs)

    async def reply_voice(self, video: Union[str, bytes, Path], caption: str = None,
                           auto_delete: int = None, object_guid: str = None,
                           reply_to_message_id: str = None, *args, **kwargs):
        return await self.reply(text=caption, object_guid=object_guid, reply_to_message_id=reply_to_message_id,
                                 file_inline=video, type='Voice', auto_delete=auto_delete, *args, **kwargs)

    async def reply_gif(self, gif: Union[str, bytes, Path], caption: str = None,
                         auto_delete: int = None, object_guid: str = None,
                         reply_to_message_id: str = None, *args, **kwargs):
        return await self.reply(text=caption, object_guid=object_guid, reply_to_message_id=reply_to_message_id,
                                 file_inline=gif, type='Gif', auto_delete=auto_delete, *args, **kwargs)

    async def reply_video_message(self, video: Union[str, bytes, Path], caption: str = None,
                                   auto_delete: int = None, object_guid: str = None,
                                   reply_to_message_id: str = None, *args, **kwargs):
        return await self.reply(text=caption, object_guid=object_guid, reply_to_message_id=reply_to_message_id,
                                 file_inline=video, type='VideoMessage', auto_delete=auto_delete, *args, **kwargs)

    async def forwards(self, to_object_guid: str, from_object_guid: str = None, message_ids=None, *args, **kwargs):
        """_forwards_
        Args:
            to_object_guid (str):
                _to object guid_.
            from_object_guid (str, optional):
                _from object guid_. Defaults to update.object_guid.
            message_ids (typing.Union[str, int, typing.List[str]], optional):
                _message ids_. Defaults to update.message_id.
        """
        if from_object_guid is None:
            from_object_guid = self.object_guid

        if message_ids is None:
            message_ids = self.message_id

        return await self.client.forward_messages(
            from_object_guid=from_object_guid,
            to_object_guid=to_object_guid,
            message_ids=message_ids,
        )

    async def download(self, file_inline=None, file=None, *args, **kwargs):
        if isinstance(file_inline, dict):
            file_inline = SocketResults(file_inline)

        return await self.client.download(file_inline or self.file_inline, file=file, *args, **kwargs)

    async def get_author(self, author_guid: str = None, *args, **kwargs):
        """_get user or author information_
        Args:
            author_guid (str, optional):
                _custom author guid_. Defaults to update.author_guid
        """
        if author_guid is None:
            author_guid = self.author_guid

        return await self.get_object(object_guid=author_guid, *args, **kwargs)

    async def get_object(self, object_guid: str = None, *args, **kwargs):
        """_get object information_
        Args:
            object_guid (str, optional):
                _custom object guid_. Defaults to update.object_guid.
        """
        if object_guid is None:
            object_guid = self.object_guid

        if self.guid_type(object_guid) == 'User':
            return await self.client.get_user_info(object_guid)
        elif self.guid_type(object_guid) == 'Group':
            return await self.client.get_group_info(object_guid)
        elif self.guid_type(object_guid) == 'Channel':
            return await self.client.get_channel_info(object_guid)

    async def get_messages(self, object_guid: str = None, message_ids=None, *args, **kwargs):
        """_get messages_
        Args:
            object_guid (str, optional):
                _custom object guid_. Defaults to update.object_guid.
            message_ids (str, int, typing.List[str]], optional):
                _message ids_. Defaults to update.message_id.
        """
        if object_guid is None:
            object_guid = self.object_guid

        if message_ids is None:
            message_ids = self.message_id

        return await self.client.get_messages_by_id(
            object_guid=object_guid,
            message_ids=message_ids,
        )

    async def delete_messages(self, object_guid: str=None, message_ids: list=None):
        """_delete messages_
        Args:
            object_guid (str, optional):
                _custom object guid_. Defaults to update.object_guid.
            message_ids (str, list, optional):
                _custom message ids_. Defaults to update.message_id.
            type(str, optional):
                the message should be deleted for everyone or not.
                Defaults to methods.messages.Global (
                    methods.messages.Local,
                    methods.messages.Global
                )
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
        if object_guid is None:
            object_guid = self.object_guid

        if object_guid.startswith('g0'):
            return await self.client.ban_group_member(object_guid, user_guid)
        elif object_guid.startswith('c0'):
            return await self.client.ban_channel_member(object_guid, user_guid)

    async def unban_member(self, object_guid: str = None, user_guid: str = None):
        if object_guid is None:
            object_guid = self.object_guid

        if object_guid.startswith('g0'):
            return await self.client.ban_group_member(object_guid, user_guid, 'Unset')
        elif object_guid.startswith('c0'):
            return await self.client.ban_channel_member(object_guid, user_guid, 'Unset')

    async def send_activity(
            self,
            activity: Literal['Typing', 'Uploading', 'Recording'] = 'Typing',
            object_guid: str = None,
    ):
        if object_guid is None:
            object_guid = self.object_guid

        return await self.client.send_chat_activity(
            object_guid=object_guid,
            activity=activity,
        )

    async def is_admin(
            self,
            object_guid: str = None,
            user_guid: str = None,
    ):
        if object_guid is None:
            object_guid = self.object_guid
        
        if user_guid is None:
            user_guid = self.object_guid

        return await self.client.user_is_admin(
            object_guid=object_guid,
            user_guid=user_guid,
        )