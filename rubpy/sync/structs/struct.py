import json
import base64
from ..gadgets import methods, thumbnail


class Struct:
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
                update[index] = Struct(update=element)

            else:
                update[index] = element
        return update

    def __init__(self, update: dict, *args, **kwargs) -> None:
        self.original_update = update

    def to_dict(self):
        return self.original_update

    def jsonify(self, indent=None, *args, **kwargs) -> str:
        result = self.original_update
        result['original_update'] = 'dict{...}'
        return json.dumps(result, indent=indent,
                          ensure_ascii=False,
                          default=lambda value: str(value))

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
                        update = Struct(update=update)

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
                    pass

        raise AttributeError(f'Struct object has no attribute {keys}')

    def guid_type(self, guid: str, *args, **kwargs) -> str:
        if isinstance(guid, str):
            if guid.startswith('u'):
                return 'User'

            elif guid.startswith('g'):
                return 'Group'

            elif guid.startswith('c'):
                return 'Channel'

    # property functions

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
            return self.find_keys(keys=['message_id',
                                        'pinned_message_id'])
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
        try:
            return self.find_keys(keys=['group_guid',
                                        'object_guid', 'channel_guid'])
        except AttributeError:
            pass

    @property
    def author_guid(self):
        try:
            return self.author_object_guid

        except AttributeError:
            pass

    def pin(self,
                  object_guid: str = None,
                  message_id: str = None,
                  action: str = methods.messages.Pin, *args, **kwargs):
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

        return self._client(
            methods.messages.SetPinMessage(
                object_guid=object_guid,
                message_id=message_id,
                action=action))

    def edit(self,
                   text: str,
                   object_guid: str = None,
                   message_id: str = None, *args, **kwargs):
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

        return self._client(
            methods.messages.EditMessage(
                object_guid=object_guid,
                message_id=message_id,
                text=text))

    def copy(self,
                   to_object_guid: str,
                   from_object_guid: str = None, message_ids=None, *args, **kwargs):
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
        
        result = self.get_messages(from_object_guid, message_ids)
        messages = []
        if result.messages:
            for message in result.messages:
                
                try:
                    file_inline = message.file_inline
                    kwargs.update(file_inline.to_dict())

                except AttributeError:
                    file_inline = None

                try:
                    thumb = thumbnail.Thumbnail(
                        base64.b64decode(message.thumb_inline), *args, **kwargs)
                    
                except AttributeError:
                    thumb = kwargs.get('thumb', True)
                                
                try:
                    message = message.sticker
                
                except AttributeError:
                    message = message.raw_text
                
                if file_inline is not None:
                    if file_inline.type not in [methods.messages.Gif,
                                                methods.messages.Sticker]:
                        file_inline = self.download(file_inline)
                        messages.append(self._client.send_message(
                            thumb=thumb,
                            message=message,
                            file_inline=file_inline,
                            object_guid=to_object_guid, *args, **kwargs))
                        continue

                messages.append(self._client.send_message(
                    message=message,
                    object_guid=to_object_guid,
                    file_inline=file_inline, *args, **kwargs))
    
        return Struct({'status': 'OK', 'messages': messages})

    def seen(self, seen_list: dict = None, *args, **kwargs):
        """_seen_
        Args:
            seen_list (dict, optional):
                _description_. Defaults t
                    {update.object_guid: update.message_id}
        """

        if seen_list is None:
            seen_list = {self.object_guid: self.message_id}
        return self._client(methods.chats.SeenChats(seen_list=seen_list))

    def reply(self,
                    message=None,
                    object_guid: str = None,
                    reply_to_message_id: str = None,
                    file_inline: str = None, *args, **kwargs):
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
            is_gif (bool, optional):
                _is it a gif file or not_. Defaults to None.
            is_image (bool, optional):
                _is it a image file or not_. Defaults to None.
            is_voice (bool, optional):
                _is it a voice file or not_. Defaults to None.
            is_music (bool, optional):
                _is it a music file or not_. Defaults to None.
            is_video (bool, optional):
                _is it a video file or not_. Defaults to None.
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

        return self._client.send_message(
            message=message,
            object_guid=object_guid,
            file_inline=file_inline,
            reply_to_message_id=reply_to_message_id, *args, **kwargs)

    def forwards(self,
                       to_object_guid: str,
                       from_object_guid: str = None,
                       message_ids=None, *args, **kwargs):
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

        return self._client(
            methods.messages.ForwardMessages(
                from_object_guid=from_object_guid,
                to_object_guid=to_object_guid,
                message_ids=message_ids))

    def download(self, file_inline=None, file=None, *args, **kwargs):
        return self._client.download_file_inline(
            file_inline or self.file_inline,
            file=file, *args, **kwargs)
    
    def get_author(self, author_guid: str = None, *args, **kwargs):
        """_get user or author information_
        Args:
            author_guid (str, optional):
                _custom author guid_. Defaults to update.author_guid
        """

        if author_guid is None:
            author_guid = self.author_guid

        return self.get_object(object_guid=author_guid, *args, **kwargs)

    def get_object(self, object_guid: str = None, *args, **kwargs):
        """_get object information_
        Args:
            object_guid (str, optional):
                _custom object guid_. Defaults to update.object_guid.
        """

        if object_guid is None:
            object_guid = self.object_guid

        if self.guid_type(object_guid) == 'User':
            return self._client(
                methods.users.GetUserInfo(
                    user_guid=object_guid))

        elif self.guid_type(object_guid) == 'Group':
            return self._client(
                methods.groups.GetGroupInfo(
                    object_guid=object_guid))

        elif self.guid_type(object_guid) == 'Channel':
            return self._client(
                methods.channels.GetChannelInfo(
                    object_guid=object_guid))

    def get_messages(self,
                           object_guid: str = None,
                           message_ids=None, *args, **kwargs):
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

        return self._client(
            methods.messages.GetMessagesByID(
                object_guid=object_guid, message_ids=message_ids))

    def delete_messages(self,
                              object_guid: str = None,
                              message_ids=None, *args, **kwargs):
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

        return self._client(
            methods.messages.DeleteMessages(
                object_guid=object_guid,
                message_ids=message_ids, *args, **kwargs))