from .. import methods
from .. import thumbnail
from base64 import b64decode
from pydantic import BaseModel
from typing import Optional, List

class FileInline(BaseModel):
    file_id: Optional[str] = None
    mime: Optional[str] = None
    dc_id: Optional[str] = None
    access_hash_rec: Optional[str] = None
    file_name: Optional[str] = None
    thumb_inline: Optional[str] = None
    music_performer: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    time: Optional[int] = None
    size: Optional[int] = None
    type: Optional[str] = None

class ForwardedFrom(BaseModel):
    type_from: Optional[str] = None
    message_id: Optional[str] = None
    object_guid: Optional[str] = None

class PollOption(BaseModel):
    options: Optional[List[str]] = []
    poll_status: Optional[dict] = None
    is_anonymous: Optional[bool] = None
    type: Optional[str] = None
    allows_multiple_answers: Optional[bool] = None

class Poll(BaseModel):
    poll_id: Optional[str] = None
    question: Optional[str] = None
    options: Optional[List[str]] = None
    poll_status: Optional[dict] = None
    is_anonymous: Optional[bool] = None
    type: Optional[str] = None
    allows_multiple_answers: Optional[bool] = None

class AvatarThumbnail(BaseModel):
    file_id: Optional[str] = None
    mime: Optional[str] = None
    dc_id: Optional[str] = None
    access_hash_rec: Optional[str] = None

class MessageData(BaseModel):
    message_id: Optional[str] = None
    text: Optional[str] = None
    file_inline: Optional[FileInline] = None
    time: Optional[str] = None
    is_edited: Optional[bool] = None
    type: Optional[str] = None
    author_type: Optional[str] = None
    author_object_guid: Optional[str] = None
    forwarded_from: Optional[ForwardedFrom] = None
    poll: Optional[Poll] = None

class AbsObject(BaseModel):
    object_guid: Optional[str] = None
    type: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_thumbnail: Optional[AvatarThumbnail] = None
    is_verified: Optional[bool] = None
    is_deleted: Optional[bool] = None

class Message(BaseModel):
    message_id: Optional[str] = None
    text: Optional[str] = None
    file_inline: Optional[FileInline] = None
    time: Optional[str] = None
    is_edited: Optional[bool] = None
    type: Optional[str] = None
    author_type: Optional[str] = None
    author_object_guid: Optional[str] = None
    forwarded_from: Optional[ForwardedFrom] = None
    poll: Optional[Poll] = None
    object_guid: Optional[str] = None
    message: Optional[MessageData] = None
    abs_object: Optional[AbsObject] = None
    last_seen_peer_mid: Optional[int] = None

class MessageUpdate(BaseModel):
    message_id: Optional[str] = None
    action: Optional[str] = None
    message: Optional[Message] = None
    updated_parameters: Optional[list] = None
    timestamp: Optional[str] = None
    prev_message_id: Optional[str] = None
    object_guid: Optional[str] = None
    type: Optional[str] = None
    state: Optional[str] = None

class LastMessage(BaseModel):
    message_id: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    author_object_guid: Optional[str] = None
    is_mine: Optional[bool] = None
    author_title: Optional[str] = None
    author_type: Optional[str] = None

class Chat(BaseModel):
    time_string: Optional[str] = None
    last_message: Optional[LastMessage] = None
    last_seen_my_mid: Optional[str] = None
    last_seen_peer_mid: Optional[int] = None
    status: Optional[str] = None
    time: Optional[int] = None
    last_message_id: Optional[str] = None

class ChatUpdate(BaseModel):
    object_guid: Optional[str] = None
    action: Optional[str] = None
    chat: Optional[Chat] = None
    updated_parameters: Optional[list] = None
    timestamp: Optional[str] = None
    type: Optional[str] = None

class SendMessage(BaseModel):
    message_update: Optional[MessageUpdate] = None
    status: Optional[str] = None
    chat_update: Optional[ChatUpdate] = None

    @classmethod
    async def set_shared_data(cls, client, message):
        cls._client = client
        cls._message = message

    @classmethod
    async def pin(cls,
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
            object_guid = cls._message.message_update.object_guid

        if message_id is None:
            message_id = cls._message.message_update.message_id

        return await cls._client(
            methods.messages.SetPinMessage(
                object_guid=object_guid,
                message_id=message_id,
                action=action))

    @classmethod
    async def edit(cls,
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
            object_guid = cls._message.message_update.object_guid

        if message_id is None:
            message_id = cls._message.message_update.message_id

        return await cls._client(
            methods.messages.EditMessage(
                object_guid=object_guid,
                message_id=message_id,
                text=text))
    
    @classmethod
    async def copy(cls,
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
            from_object_guid = cls._message.message_update.object_guid

        if message_ids is None:
            message_ids = cls._message.message_update.message_id
        
        result = await cls.get_messages(from_object_guid, message_ids)
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
                        b64decode(message.thumb_inline), *args, **kwargs)
                    
                except AttributeError:
                    thumb = kwargs.get('thumb', True)
                                
                try:
                    message = message.sticker
                
                except AttributeError:
                    message = message.raw_text
                
                if file_inline is not None:
                    if file_inline.type not in [methods.messages.Gif,
                                                methods.messages.Sticker]:
                        file_inline = await cls.download(file_inline)
                        messages.append(await cls._client.send_message(
                            thumb=thumb,
                            message=message,
                            file_inline=file_inline,
                            object_guid=to_object_guid, *args, **kwargs))
                        continue

                messages.append(await cls._client.send_message(
                    message=message,
                    object_guid=to_object_guid,
                    file_inline=file_inline, *args, **kwargs))
    
        return {'status': 'OK', 'messages': messages}

    @classmethod
    async def seen(cls, seen_list: dict = None, *args, **kwargs):
        """_seen_
        Args:
            seen_list (dict, optional):
                _description_. Defaults t
                    {update.object_guid: update.message_id}
        """

        if seen_list is None:
            seen_list = {cls._message.message_update.object_guid: cls._message.message_update.message_id}
        return await cls._client(methods.chats.SeenChats(seen_list=seen_list))

    @classmethod
    async def reply(cls,
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
            object_guid = cls._message.message_update.object_guid

        if message_id is None:
            message_id = cls._message.message_update.message_id

        return await cls._client.send_message(
            message=message,
            object_guid=object_guid,
            file_inline=file_inline,
            reply_to_message_id=reply_to_message_id, *args, **kwargs)

    @classmethod
    async def forwards(cls,
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
            from_object_guid = cls._message.message_update.object_guid

        if message_ids is None:
            message_ids = cls._message.message_update.message_id

        return await cls._client(
            methods.messages.ForwardMessages(
                from_object_guid=from_object_guid,
                to_object_guid=to_object_guid,
                message_ids=message_ids))

    @classmethod
    async def download(cls, file_inline=None, file=None, *args, **kwargs):
        return await cls._client.download_file_inline(
            file_inline or cls._message.file_inline,
            file=file, *args, **kwargs)

    @classmethod
    async def get_author(cls, author_guid: str = None, *args, **kwargs):
        """_get user or author information_
        Args:
            author_guid (str, optional):
                _custom author guid_. Defaults to update.author_guid
        """

        if author_guid is None:
            author_guid = cls._message.message_update.message.author_object_guid

        return await cls.get_object(object_guid=author_guid, *args, **kwargs)

    @classmethod
    async def get_object(cls, object_guid: str = None, *args, **kwargs):
        """_get object information_
        Args:
            object_guid (str, optional):
                _custom object guid_. Defaults to update.object_guid.
        """

        if object_guid is None:
            object_guid = cls._message.message_update.object_guid


        if cls.guid_type(object_guid) == 'User':
            return await cls._client(
                methods.users.GetUserInfo(
                    user_guid=object_guid))

        elif cls.guid_type(object_guid) == 'Group':
            return await cls._client(
                methods.groups.GetGroupInfo(
                    object_guid=object_guid))

        elif cls.guid_type(object_guid) == 'Channel':
            return await cls._client(
                methods.channels.GetChannelInfo(
                    object_guid=object_guid))

    @classmethod
    async def get_message(cls,
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
            object_guid = cls._message.message_update.object_guid

        if message_ids is None:
            message_ids = cls._message.message_update.message_id

        return await cls._client(
            methods.messages.GetMessagesByID(
                object_guid=object_guid, message_ids=message_ids))

    @classmethod
    async def delete(cls,
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
            object_guid = cls._message.message_update.object_guid

        if message_ids is None:
            message_ids = cls._message.message_update.message_id

        return await cls._client(
            methods.messages.DeleteMessages(
                object_guid=object_guid,
                message_ids=message_ids, *args, **kwargs))

class EditMessage(BaseModel):
    message_update: Optional[MessageUpdate] = None
    chat_update: Optional[ChatUpdate] = None
    
    @classmethod
    async def set_shared_data(cls, client, message):
        cls._client = client
        cls._message = message

    @classmethod
    async def pin(cls,
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
            object_guid = cls._message.message_update.object_guid

        if message_id is None:
            message_id = cls._message.message_update.message_id

        return await cls._client(
            methods.messages.SetPinMessage(
                object_guid=object_guid,
                message_id=message_id,
                action=action))

    @classmethod
    async def edit(cls,
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
            object_guid = cls._message.message_update.object_guid

        if message_id is None:
            message_id = cls._message.message_update.message_id

        return await cls._client(
            methods.messages.EditMessage(
                object_guid=object_guid,
                message_id=message_id,
                text=text))
    
    @classmethod
    async def copy(cls,
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
            from_object_guid = cls._message.message_update.object_guid

        if message_ids is None:
            message_ids = cls._message.message_update.message_id
        
        result = await cls.get_messages(from_object_guid, message_ids)
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
                        b64decode(message.thumb_inline), *args, **kwargs)
                    
                except AttributeError:
                    thumb = kwargs.get('thumb', True)
                                
                try:
                    message = message.sticker
                
                except AttributeError:
                    message = message.raw_text
                
                if file_inline is not None:
                    if file_inline.type not in [methods.messages.Gif,
                                                methods.messages.Sticker]:
                        file_inline = await cls.download(file_inline)
                        messages.append(await cls._client.send_message(
                            thumb=thumb,
                            message=message,
                            file_inline=file_inline,
                            object_guid=to_object_guid, *args, **kwargs))
                        continue

                messages.append(await cls._client.send_message(
                    message=message,
                    object_guid=to_object_guid,
                    file_inline=file_inline, *args, **kwargs))
    
        return {'status': 'OK', 'messages': messages}

    @classmethod
    async def seen(cls, seen_list: dict = None, *args, **kwargs):
        """_seen_
        Args:
            seen_list (dict, optional):
                _description_. Defaults t
                    {update.object_guid: update.message_id}
        """

        if seen_list is None:
            seen_list = {cls._message.message_update.object_guid: cls._message.message_update.message_id}
        return await cls._client(methods.chats.SeenChats(seen_list=seen_list))

    @classmethod
    async def reply(cls,
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
            object_guid = cls._message.message_update.object_guid

        if message_id is None:
            message_id = cls._message.message_update.message_id

        return await cls._client.send_message(
            message=message,
            object_guid=object_guid,
            file_inline=file_inline,
            reply_to_message_id=reply_to_message_id, *args, **kwargs)

    @classmethod
    async def forwards(cls,
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
            from_object_guid = cls._message.message_update.object_guid

        if message_ids is None:
            message_ids = cls._message.message_update.message_id

        return await cls._client(
            methods.messages.ForwardMessages(
                from_object_guid=from_object_guid,
                to_object_guid=to_object_guid,
                message_ids=message_ids))

    @classmethod
    async def download(cls, file_inline=None, file=None, *args, **kwargs):
        return await cls._client.download_file_inline(
            file_inline or cls._message.file_inline,
            file=file, *args, **kwargs)

    @classmethod
    async def get_author(cls, author_guid: str = None, *args, **kwargs):
        """_get user or author information_
        Args:
            author_guid (str, optional):
                _custom author guid_. Defaults to update.author_guid
        """

        if author_guid is None:
            author_guid = cls._message.message_update.message.author_object_guid

        return await cls.get_object(object_guid=author_guid, *args, **kwargs)

    @classmethod
    async def get_object(cls, object_guid: str = None, *args, **kwargs):
        """_get object information_
        Args:
            object_guid (str, optional):
                _custom object guid_. Defaults to update.object_guid.
        """

        if object_guid is None:
            object_guid = cls._message.message_update.object_guid


        if cls.guid_type(object_guid) == 'User':
            return await cls._client(
                methods.users.GetUserInfo(
                    user_guid=object_guid))

        elif cls.guid_type(object_guid) == 'Group':
            return await cls._client(
                methods.groups.GetGroupInfo(
                    object_guid=object_guid))

        elif cls.guid_type(object_guid) == 'Channel':
            return await cls._client(
                methods.channels.GetChannelInfo(
                    object_guid=object_guid))

    @classmethod
    async def get_message(cls,
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
            object_guid = cls._message.message_update.object_guid

        if message_ids is None:
            message_ids = cls._message.message_update.message_id

        return await cls._client(
            methods.messages.GetMessagesByID(
                object_guid=object_guid, message_ids=message_ids))

    @classmethod
    async def delete(cls,
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
            object_guid = cls._message.message_update.object_guid

        if message_ids is None:
            message_ids = cls._message.message_update.message_id

        return await cls._client(
            methods.messages.DeleteMessages(
                object_guid=object_guid,
                message_ids=message_ids, *args, **kwargs))

class DeleteMessages(BaseModel):
    chat_update: Optional[ChatUpdate] = None
    message_updates: Optional[List[MessageUpdate]] = []
    _client: Optional[str] = None
    original_update: Optional[str] = None

class RequestSendFile(BaseModel):
    id: Optional[str] = None
    dc_id: Optional[str] = None
    access_hash_send: Optional[str] = None
    upload_url: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class ForwardMessages(BaseModel):
    chat_update: Optional[ChatUpdate] = None
    message_updates: Optional[List[MessageUpdate]] = []
    status: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class PollStatus(BaseModel):
    state: Optional[str] = None
    selection_index: Optional[int] = None
    percent_vote_options: Optional[list[int]] = None
    total_vote: Optional[int] = None
    show_total_votes: Optional[bool] = None

class VotePoll(BaseModel):
    poll_status: Optional[PollStatus] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class SetPinMessage(BaseModel):
    chat_update: Optional[ChatUpdate] = None
    status: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class GetMessagesUpdates(BaseModel):
    updated_messages: Optional[List[MessageUpdate]] = []
    new_state: Optional[int] = None
    status: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class SearchGlobalMessages(BaseModel):
    messages: Optional[List[Message]] = []
    next_start_id: Optional[str] = None
    has_continue: Optional[bool] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class GetMessagesByID(BaseModel):
    messages: Optional[List[Message]] = []
    timestamp: Optional[int] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class GetMessagesInterval(BaseModel):
    messages: Optional[List[Message]] = []
    state: Optional[str] = None
    new_has_continue: Optional[bool] = None
    old_has_continue: Optional[bool] = None
    new_min_id: Optional[int] = None
    old_max_id: Optional[int] = None
    timestamp: Optional[str] = None
    _client: Optional[str] = None
    original_update: Optional[str] = None

class Reactions(BaseModel):
    user_guids: Optional[List] = []
    reaction_count: Optional[int] = None
    emoji_char: Optional[str] = None
    reaction_id: Optional[int] = None
    is_selected: Optional[bool] = None

class Reacion(BaseModel):
    reactions: Optional[List[Reactions]] = []