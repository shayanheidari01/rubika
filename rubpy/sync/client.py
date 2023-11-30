from .gadgets import exceptions, methods, thumbnail
from .sessions import StringSession, SQLiteSession
from .network import Connection, Proxies
from . import __name__ as logger_name
from mutagen.mp3 import MP3
from .structs import Struct
from .crypto import Crypto
from io import BytesIO
from re import compile
import logging
import os


class Client:
    configuire = {
        'package': 'web.rubika.ir',
        'platform': 'Web',
        'app_name': 'Main',
        'user_agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko)'
                       'Chrome/102.0.0.0 Safari/537.36'),
        'api_version': '6',
        'app_version': '4.4.5'
    }

    def __init__(self,
                 session,
                 proxy=None,
                 logger=None,
                 timeout=20,
                 lang_code='fa',
                 user_agent=None,
                 request_retries=5, *args, **kwargs):

        if isinstance(session, str):
            session = SQLiteSession(session)

        elif not isinstance(session, StringSession):
            raise TypeError('The given session must be a '
                            'str or [rubpy.sessions.StringSession]')

        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger_name)

        if proxy and not isinstance(proxy, Proxies):
            raise TypeError(
                'The given proxy must be a [rubpy.network.Proxies]')

        self._dcs = None
        self._key = None
        self._auth = None
        self._guid = None
        self._proxy = proxy
        self._logger = logger
        self._timeout = timeout
        self._session = session
        self._handlers = {}
        self._request_retries = request_retries
        self._user_agent = user_agent or self.configuire['user_agent']
        self._platform = {
            'package': kwargs.get('package', self.configuire['package']),
            'platform': kwargs.get('platform', self.configuire['platform']),
            'app_name': kwargs.get('app_name', self.configuire['app_name']),
            'app_version': kwargs.get('app_version',
                                      self.configuire['app_version']),
            'lang_code': lang_code}

    def __call__(self, request: object):
        try:
            result = self._connection.execute(request)

            if result.__name__ == 'signIn' and result.status == 'OK':
                result.auth = Crypto.decrypt_RSA_OAEP(self._private_key, result.auth)
                self._key = Crypto.passphrase(result.auth)
                self._auth = result.auth
                self._session.insert(
                    auth=self._auth,
                    guid=result.user.user_guid,
                    user_agent=self._user_agent,
                    phone_number=result.user.phone,
                    private_key=self._private_key)

                self(
                    methods.authorisations.RegisterDevice(
                        self._user_agent,
                        lang_code=self._platform['lang_code'],
                        app_version=self._platform['app_version'])
                )

            return result

        except AttributeError:
            raise exceptions.NoConnection(
                'You must first connect the Client'
                ' with the *.connect() method')

    def __enter__(self):
        return self.start(phone_number=None)

    def __exit__(self, *args, **kwargs):
        return self.disconnect()

    def start(self, phone_number: str, *args, **kwargs):
        if not hasattr(self, '_connection'):
            self.connect()

        try:
            self._logger.info('user info', extra={'data': self.get_me()})

        except (exceptions.NotRegistrred, exceptions.InvalidInput):
            self._logger.debug('user not registered!')
            if phone_number is None:
                phone_number = input('Phone Number: ')
                is_phone_number_true = True
                while is_phone_number_true:
                    if input(f'Is the {phone_number} correct[y or n] > ').lower() == 'y':
                        is_phone_number_true = False
                    else:
                        phone_number = input('Phone Number: ')

            if phone_number.startswith('0'):
                phone_number = '98{}'.format(phone_number[1:])
            elif phone_number.startswith('+98'):
                phone_number = phone_number[1:]
            elif phone_number.startswith('0098'):
                phone_number = phone_number[2:]

            result = self(
                methods.authorisations.SendCode(
                    phone_number=phone_number, *args, **kwargs))

            if result.status == 'SendPassKey':
                while True:
                    pass_key = input(f'Password [{result.hint_pass_key}] > ')
                    result = self(
                        methods.authorisations.SendCode(
                            phone_number=phone_number,
                            pass_key=pass_key, *args, **kwargs))

                    if result.status == 'OK':
                        break

            public_key, self._private_key = Crypto.create_keys()
            while True:
                phone_code = input('Code: ')
                result = self(
                    methods.authorisations.SignIn(
                        phone_code=phone_code,
                        phone_number=phone_number,
                        phone_code_hash=result.phone_code_hash,
                        public_key=public_key,
                        *args, **kwargs))

                if result.status == 'OK':
                    break

        return self

    def connect(self):
        self._connection = Connection(client=self)
        information = self._session.information()
        self._logger.info(f'the session information was read {information}')
        if information:
            self._auth = information[1]
            self._guid = information[2]
            self._private_key = information[4]
            if isinstance(information[3], str):
                self._user_agent = information[3]

        return self

    def disconnect(self):
        try:
            self._connection.close()
            self._logger.info(f'the client was disconnected')

        except AttributeError:
            raise exceptions.NoConnection(
                'You must first connect the Client'
                ' with the *.connect() method')

    def run_until_disconnected(self):
        return self._connection.receive_updates()

    def on(self, handler):
        def MetaHandler(func):
            self.add_handler(func, handler)
            return func
        return MetaHandler

    def add_handler(self, func, handler):
        self._handlers[func] = handler

    def remove_handler(self, func):
        try:
            self._handlers.pop(func)
        except KeyError:
            pass

    def get_me(self, *args, **kwargs):
        return self(methods.users.GetUserInfo(self._guid))

    def upload(self, file, *args, **kwargs):
        return self._connection.upload_file(file=file, *args, **kwargs)

    def download_file_inline(self, file_inline, save_as: str = None, chunk_size: int = 131072, callback=None, *args, **kwargs):
        result = self._connection.download(
            file_inline.dc_id,
            file_inline.file_id,
            file_inline.access_hash_rec,
            file_inline.size,
            chunk=chunk_size,
            callback=callback)

        if isinstance(save_as, str):
            with open(save_as, 'wb+') as _file:
                _file.write(result)
                return save_as

        return result


# ---------------- Users Methods ----------------

    def get_user_info(self, user_guid: str):
        return self(methods.users.GetUserInfo(user_guid))

    def block_user(self, user_guid: str):
        return self(methods.users.SetBlockUser(user_guid, 'Block'))

    def unblock_user(self, user_guid: str):
        return self(methods.users.SetBlockUser(user_guid, 'Unblock'))

    def delete_user_chat(self, user_guid: str, last_deleted_message_id: str):
        return self(methods.users.DeleteUserChat(user_guid, last_deleted_message_id))

    def check_user_username(self, username: str):
        return self(methods.users.CheckUserUsername(username.replace('@', '')))

# ---------------- Chats Methods ----------------

    def upload_avatar(self, object_guid: str, main_file_id: str, thumbnail_file_id: str):
        return self(methods.chats.UploadAvatar(object_guid, main_file_id, thumbnail_file_id))

    def delete_avatar(self, object_guid: str, avatar_id: str):
        return self(methods.chats.DeleteAvatar(object_guid, avatar_id))

    def get_avatars(self, object_guid: str):
        return self(methods.chats.GetAvatars(object_guid))

    def get_chats(self, start_id: int = None):
        return self(methods.chats.GetChats(start_id))

    def seen_chats(self, seen_list: dict):
        return self(methods.chats.SeenChats(seen_list))

    def get_chat_ads(self, state: int):
        return self(methods.chats.GetChatAds(state))

    def set_action_chat(self, object_guid: str, action: str):
        '''
        alloweds: ["Mute", "Unmute"]
        result = client.set_action_chat('object_guid', 'Mute')
        print(result)
        '''
        return self(methods.chats.SetActionChat(object_guid, action))

    def get_chats_updates(self, state: int = None):
        return self(methods.chats.GetChatsUpdates(state))

    def send_chat_activity(self, object_guid: str, activity: str = None):
        return self(methods.chats.SendChatActivity(object_guid, activity))

    def delete_chat_history(self, object_guid: str):
        return self(methods.chats.DeleteChatHistory(object_guid))

    def search_chat_messages(self, object_guid: str, search_text: str, type: str = 'Hashtag'):
        return self(methods.chats.SearchChatMessages(object_guid, search_text, type))

# ---------------- Extras Methods ----------------

    def search_global_objects(self, search_text: str):
        return self(methods.extras.SearchGlobalObjects(search_text))

    def get_abs_objects(self, objects_guids: list):
        return self(methods.extras.GetAbsObjects(objects_guids))

    def get_object_by_username(self, username: str):
        return self(methods.extras.GetObjectByUsername(username.replace('@', '')))

    def get_link_from_app_url(self, app_url: str):
        return self(methods.extras.GetLinkFromAppUrl(app_url))

    def create_voice_call(self, object_guid: str):
        if object_guid.startswith('c'):
            return self(methods.channels.CreateChannelVoiceChat(object_guid))
        elif object_guid.startswith('g'):
            return self(methods.groups.CreateGroupVoiceChat(object_guid))
        else:
            print('Invalid Object Guid')
            return False

    def set_voice_chat_setting(self, object_guid: str, voice_chat_id: str, title: str = None):
        if object_guid.startswith('c'):
            return self(methods.channels.SetChannelVoiceChatSetting(object_guid, voice_chat_id, title, ['title']))
        elif object_guid.startswith('g'):
            return self(methods.groups.SetGroupVoiceChatSetting(object_guid, voice_chat_id, title, ['title']))
        else:
            print('Invalid Object Guid')
            return False

# ---------------- Groups Methods ----------------

    def add_group(self, title: str, member_guids: list):
        return self(methods.groups.AddGroup(title, member_guids))

    def join_group(self, link: str):
        return self(methods.groups.JoinGroup(link))

    def leave_group(self, group_guid: str):
        return self(methods.groups.LeaveGroup(group_guid))

    def remove_group(self, group_guid: str):
        return self(methods.groups.RemoveGroup(group_guid))

    def get_group_info(self, group_guid: str):
        return self(methods.groups.GetGroupInfo(group_guid))

    def get_group_link(self, group_guid: str):
        return self(methods.groups.GetGroupLink(group_guid))

    def set_group_link(self, group_guid: str):
        return self(methods.groups.SetGroupLink(group_guid))

    def edit_group_info(self,
         group_guid: str,
         title: str = None,
         description: str = None,
         chat_history_for_new_members: str = None,
     ):
        updated_parameters = []

        if title:
            updated_parameters.append('title')
        if description:
            updated_parameters.append('description')
        if chat_history_for_new_members:
            updated_parameters.append('chat_history_for_new_members')

        return self(methods.groups.EditGroupInfo(
            group_guid, updated_parameters, title, description, chat_history_for_new_members))

    def set_group_admin(self,
        group_guid: str,
        member_guid: str,
        access_list: list,
        action: str = 'SetAdmin',
    ):
        return self(methods.groups.SetGroupAdmin(group_guid, member_guid, access_list, action))

    def ban_group_member(self, group_guid: str, member_guid: str):
        return self(methods.groups.BanGroupMember(group_guid, member_guid, 'Set'))

    def unban_group_member(self, group_guid: str, member_guid: str):
        return self(methods.groups.BanGroupMember(group_guid, member_guid, 'Unset'))

    def add_group_members(self, group_guid: str, member_guids: list):
        return self(methods.groups.AddGroupMembers(group_guid, member_guids))

    def get_group_all_members(self, group_guid: str, search_text: str = None, start_id: int = None):
        return self(methods.groups.GetGroupAllMembers(group_guid, search_text, start_id))

    def get_group_admin_members(self, group_guid: str, start_id: int = None):
        return self(methods.groups.GetGroupAdminMembers(group_guid, start_id))

    def get_group_mention_list(self, group_guid: str, search_mention: str = None):
        return self(methods.groups.GetGroupMentionList(group_guid, search_mention))

    def get_group_default_access(self, group_guid: str):
        return self(methods.groups.GetGroupDefaultAccess(group_guid))

    def set_group_default_access(self, group_guid: str, access_list: list):
        return self(methods.groups.SetGroupDefaultAccess(group_guid, access_list))

    def group_preview_by_join_link(self, group_link: str):
        return self(methods.groups.GroupPreviewByJoinLink(group_link))

    def delete_no_access_group_chat(self, group_guid: str):
        return self(methods.groups.DeleteNoAccessGroupChat(group_guid))

    def get_group_admin_access_list(self, group_guid: str, member_guid: str):
        return self(methods.groups.GetGroupAdminAccessList(group_guid, member_guid))

    def set_group_timer(self, group_guid: str, time: int):
        return self(methods.groups.EditGroupInfo(group_guid, slow_mode=time, updated_parameters=['slow_mode']))

# ---------------- Messages Methods ----------------

    def custom_send_message(self,
        object_guid: str,
        message=None,
        reply_to_message_id: str = None,
        file: bytes = None,
        file_inline: dict = None,
        *args, **kwargs
    ) -> dict:
        if compile(r'(?i)^(me|self|cloud)$').match(object_guid):
            object_guid = self._guid

        if file:
            file = self.upload(file, *args, **kwargs)
            for key, value in file_inline.items():
                file[key] = value

        return self(
            methods.messages.SendMessage(
                object_guid,
                message=message,
                file_inline=file,
                reply_to_message_id=reply_to_message_id))

    def send_message(self,
        object_guid: str,
        message=None,
        reply_to_message_id: str = None,
        file_inline=None,
        type: str = methods.messages.File,
        thumb: bool = True, *args, **kwargs
    ):
        """_send message_

        Args:
            object_guid (str):
                _object guid_

            message (Any, optional):
                _message or cation or sticker_ . Defaults to None.

            reply_to_message_id (str, optional):
                _reply to message id_. Defaults to None.

            file_inline (typing.Union[pathlib.Path, bytes], optional):
                _file_. Defaults to None.

            type (str, optional):
                _file type_. Defaults to methods.messages.File.(
                    methods.messages.Gif,
                    methods.messages.Image,
                    methods.messages.Voice,
                    methods.messages.Music,
                    methods.messages.Video
                )

            thumb (bool, optional):
                if value is "True",
                    the lib will try to build the thumb ( require cv2 )
                if value is thumbnail.Thumbnail, to set custom
                Defaults to True.
        """

        if compile(r'(?i)^(me|self|cloud)$').match(object_guid):
            object_guid = self._guid

        if file_inline is not None:
            if not isinstance(file_inline, Struct):
                if isinstance(file_inline, str):
                    with open(file_inline, 'rb') as file:
                        kwargs['file_name'] = kwargs.get(
                            'file_name', os.path.basename(file_inline))
                        file_inline = file.read()

                if thumb is True:
                    if type == methods.messages.Image:
                        thumb = thumbnail.MakeThumbnail(file_inline)

                    elif type in [methods.messages.Gif, methods.messages.Video]:
                        thumb = thumbnail.MakeThumbnail.from_video(file_inline)

                    if thumb.image is None:
                        type = methods.messages.File
                        thumb = None

                # the problem will be fixed in the next version #debug
                # to avoid getting InputError
                # values are not checked in Rubika (optional)
                file_inline = self.upload(file_inline, *args, **kwargs)
                file_inline['type'] = type
                file_inline['time'] = kwargs.get('time', 1)
                file_inline['width'] = kwargs.get('width', 200)
                file_inline['height'] = kwargs.get('height', 200)
                file_inline['music_performer'] = kwargs.get('performer', '')

                if isinstance(thumb, thumbnail.Thumbnail):
                    file_inline['time'] = thumb.seconds
                    file_inline['width'] = thumb.width
                    file_inline['height'] = thumb.height
                    file_inline['thumb_inline'] = thumb.to_base64()

        return self(
            methods.messages.SendMessage(
                object_guid,
                message=message,
                file_inline=file_inline,
                reply_to_message_id=reply_to_message_id))

    def send_photo(self,
        object_guid: str,
        photo: bytes,
        caption: str = None,
        file_name: str = None,
        width: int = None,
        height: int = None,
        thumb_inline: str = None,
        reply_to_message_id: str = None,
        *args,
        **kwargs,
    ):
        if compile(r'(?i)^(me|self|cloud)$').match(object_guid):
            object_guid = self._guid

        if isinstance(photo, str):
            with open(photo, 'rb') as file:
                file_name = os.path.basename(photo)
                kwargs['file_name'] = kwargs.get('file_name', file_name)
                photo = file.read()

        else:
            kwargs['file_name'] = kwargs.get('file_name', file_name)

        file_inline = self.upload(photo, *args, **kwargs)
        file_inline['type'] = 'Image'
        thumb = thumbnail.MakeThumbnail(photo)

        if isinstance(thumb, thumbnail.Thumbnail):
            file_inline['width'] = thumb.width
            file_inline['height'] = thumb.height
            file_inline['thumb_inline'] = thumb.to_base64()
        else:
            file_inline['width'] = width
            file_inline['height'] = height
            file_inline['thumb_inline'] = thumb_inline

        return self(
            methods.messages.SendMessage(
                object_guid,
                message=caption,
                file_inline=file_inline,
                reply_to_message_id=reply_to_message_id))

    def send_file(self,
        object_guid: str,
        file: bytes,
        caption: str = None,
        file_name: str = None,
        reply_to_message_id: str = None,
        *args,
        **kwargs,
    ):
        if compile(r'(?i)^(me|self|cloud)$').match(object_guid):
            object_guid = self._guid

        if isinstance(file, str):
            with open(file, 'rb') as ofile:
                file_name = os.path.basename(file)
                kwargs['file_name'] = kwargs.get('file_name', file_name)
                file = ofile.read()
        else:
            kwargs['file_name'] = kwargs.get('file_name', file_name)

        file_inline = self.upload(file, *args, **kwargs)
        file_inline['type'] = 'File'

        return self(
            methods.messages.SendMessage(
                object_guid,
                message=caption,
                file_inline=file_inline,
                reply_to_message_id=reply_to_message_id))

    def send_gif(self,
        object_guid: str,
        gif: bytes,
        caption: str = None,
        file_name: str = None,
        thumb_inline: str = None,
        time: str = None,
        width: int = None,
        height: int = None,
        reply_to_message_id: str = None,
        *args,
        **kwargs,
    ):
        if compile(r'(?i)^(me|self|cloud)$').match(object_guid):
            object_guid = self._guid

        if isinstance(gif, str):
            with open(gif, 'rb') as file:
                file_name = os.path.basename(gif)
                kwargs['file_name'] = kwargs.get('file_name', file_name)
                file = file.read()
        else:
            kwargs['file_name'] = kwargs.get('file_name', file_name)

        file_inline = self.upload(gif, *args, **kwargs)
        file_inline['type'] = 'Gif'
        thumb = thumbnail.MakeThumbnail.from_video(gif)

        if isinstance(thumb, thumbnail.Thumbnail):
            file_inline['time'] = thumb.seconds
            file_inline['width'] = thumb.width
            file_inline['height'] = thumb.height
            file_inline['thumb_inline'] = thumb.to_base64()
        else:
            file_inline['time'] = time
            file_inline['width'] = width
            file_inline['height'] = height
            file_inline['thumb_inline'] = thumb_inline

        return self(
            methods.messages.SendMessage(
                object_guid,
                message=caption,
                file_inline=file_inline,
                reply_to_message_id=reply_to_message_id))

    def send_video(self,
        object_guid: str,
        video: bytes,
        caption: str = None,
        file_name: str = None,
        thumb_inline: str = None,
        time: str = None,
        width: int = None,
        height: int = None,
        reply_to_message_id: str = None,
        *args,
        **kwargs,
    ):
        if compile(r'(?i)^(me|self|cloud)$').match(object_guid):
            object_guid = self._guid

        if isinstance(video, str):
            with open(video, 'rb') as file:
                file_name = os.path.basename(video)
                kwargs['file_name'] = kwargs.get('file_name', file_name)
                video = file.read()
        else:
            kwargs['file_name'] = kwargs.get('file_name', file_name)

        file_inline = self.upload(video, *args, **kwargs)
        file_inline['type'] = 'Video'
        thumb = thumbnail.MakeThumbnail.from_video(video)

        if isinstance(thumb, thumbnail.Thumbnail):
            file_inline['time'] = thumb.seconds
            file_inline['width'] = thumb.width
            file_inline['height'] = thumb.height
            file_inline['thumb_inline'] = thumb.to_base64()
        else:
            file_inline['time'] = time
            file_inline['width'] = width
            file_inline['height'] = height
            file_inline['thumb_inline'] = thumb_inline

        return self(
            methods.messages.SendMessage(
                object_guid,
                message=caption,
                file_inline=file_inline,
                reply_to_message_id=reply_to_message_id))

    def send_music(self,
        object_guid: str,
        music: bytes,
        caption: str = None,
        file_name: str = None,
        time: str = None,
        performer: str = None,
        reply_to_message_id: str = None,
        *args,
        **kwargs,
    ):
        if compile(r'(?i)^(me|self|cloud)$').match(object_guid):
            object_guid = self._guid

        if isinstance(music, bytes):
            kwargs['file_name'] = kwargs.get('file_name', file_name)
        else:
            with open(music, 'rb') as file:
                kwargs['file_name'] = kwargs.get('file_name', os.path.basename(music))
                music = file.read()

        file_inline = self.upload(music, *args, **kwargs)
        file_inline['type'] = 'Music'
        file_inline['auto_play'] = False
        file_inline['music_performer'] = kwargs.get('performer', performer or '')
        file = BytesIO()
        file.write(music)
        file.seek(0)
        file_inline['time'] = time or MP3(file).info.length * 1000

        return self(
            methods.messages.SendMessage(
                object_guid,
                message=caption,
                file_inline=file_inline,
                reply_to_message_id=reply_to_message_id))

    def send_voice(self,
        object_guid: str,
        voice: bytes,
        caption: str = None,
        file_name: str = None,
        time: str = None,
        reply_to_message_id: str = None,
        *args,
        **kwargs,
    ):
        if compile(r'(?i)^(me|self|cloud)$').match(object_guid):
            object_guid = self._guid

        if isinstance(voice, str):
            with open(voice, 'rb') as file:
                file_name = os.path.basename(voice)
                kwargs['file_name'] = kwargs.get('file_name', file_name)
                file = file.read()
        else:
            kwargs['file_name'] = kwargs.get('file_name', file_name)

        file_inline = self.upload(voice, *args, **kwargs)
        file_inline['type'] = 'Voice'
        file_inline['mime'] = 'ogg'
        file_inline['auto_play'] = False
        file = BytesIO()
        file.write(voice)
        file.seek(0)
        file_inline['time'] = str(time or MP3(file).info.length * 1000)

        return self(
            methods.messages.SendMessage(
                object_guid,
                message=caption,
                file_inline=file_inline,
                reply_to_message_id=reply_to_message_id))

    def edit_message(self, object_guid: str, message_id: str, text: str):
        return self(methods.messages.EditMessage(object_guid, message_id, text))

    def delete_messages(self, object_guid: str, message_ids: list, type: str = 'Global'):
        return self(methods.messages.DeleteMessages(object_guid, message_ids, type))

    def request_send_file(self, file_name: str, size: int, mime: str):
        return self(methods.messages.RequestSendFile(file_name, size, mime))

    def forward_messages(self, from_object_guid: str, to_object_guid: str, message_ids: list):
        return self(methods.messages.ForwardMessages(from_object_guid, to_object_guid, message_ids))

    def create_poll(self,
            object_guid: str,
            question: str,
            options: list,
            type: str = 'Regular',
            is_anonymous: bool = True,
            allows_multiple_answers: bool = False,
            correct_option_index: int = 0,
            explanation: str = None,
            reply_to_message_id: int = 0,
    ):
        if type == 'Regular':
            return self(methods.messages.CreatePoll(
                object_guid=object_guid,
                question=question,
                options=options,
                allows_multiple_answers=allows_multiple_answers,
                is_anonymous=is_anonymous,
                reply_to_message_id=reply_to_message_id,
                type=type,
            ))
        else:
            return self(methods.messages.CreatePoll(
                object_guid=object_guid,
                question=question,
                options=options,
                allows_multiple_answers=allows_multiple_answers,
                is_anonymous=is_anonymous,
                reply_to_message_id=reply_to_message_id,
                correct_option_index=correct_option_index,
                explanation=explanation,
                type=type,
            ))

    def vote_poll(self, poll_id: str, selection_index: int):
        return self(methods.messages.VotePoll(poll_id, selection_index))

    def get_poll_status(self, poll_id: str):
        return self(methods.messages.GetPollStatus(poll_id))

    def get_poll_option_voters(self, poll_id: str, selection_index: int, start_id: int = None):
        return self(methods.messages.GetPollOptionVoters(poll_id, selection_index, start_id))

    def set_pin_message(self, object_guid: str, message_id: str, action: str = 'Pin'):
        return self(methods.messages.SetPinMessage(object_guid, message_id, action))

    def unset_pin_message(self, object_guid: str, message_id: str, action: str = 'Unpin'):
        return self(methods.messages.SetPinMessage(object_guid, message_id, action))

    def get_messages_updates(self, object_guid: str, state: int = None):
        return self(methods.messages.GetMessagesUpdates(object_guid, state))

    def search_global_messages(self, search_text: str, type: str = 'Text'):
        return self(methods.messages.SearchGlobalMessages(search_text, type))

    def click_message_url(self, object_guid: str, message_id: str, link_url: str):
        return self(methods.messages.ClickMessageUrl(object_guid, message_id, link_url))

    def get_messages_by_ID(self, object_guid: str, message_ids: list):
        return self(methods.messages.GetMessagesByID(object_guid, message_ids))

    def get_messages(self, object_guid: str, min_id: int, max_id: int, sort: str = 'FromMin', limit: int = 10):
        return self(methods.messages.GetMessages(object_guid, min_id, max_id, sort, limit))

    def get_messages_interval(self, object_guid: str, middle_message_id: str):
        return self(methods.messages.GetMessagesInterval(object_guid, middle_message_id))

    def get_message_url(self, object_guid: str, message_id: int):
        if type(message_id) == str:
            message_id = int(message_id)
        return self(methods.messages.GetMessageShareUrl(object_guid, message_id))

# ---------------- Channels Methods ----------------

    def add_channel(self, title: str, description: str = None):
        return self(methods.channels.AddChannel(title, description))

    def remove_channel(self, channel_guid: str):
        return self(methods.channels.RemoveChannel(channel_guid))

    def get_channel_info(self, channel_guid: str):
        return self(methods.channels.GetChannelInfo(channel_guid))

    def edit_channel_info(self,
            channel_guid: str,
            title: str = None,
            description: str = None,
            channel_type: str = None,
            sign_messages: str = None,
    ):
        updated_parameters = []

        if title:
            updated_parameters.append('title')
        if description:
            updated_parameters.append('description')
        if channel_type:
            updated_parameters.append('channel_type')
        if sign_messages:
            updated_parameters.append('sign_messages')

        return self(methods.channels.EditChannelInfo(
            channel_guid, updated_parameters, title, description, channel_type, sign_messages))

    def join_channel(self, channel_guid: str):
        return self(methods.channels.JoinChannelAction(channel_guid, 'Join'))

    def leave_channel(self, channel_guid: str):
        return self(methods.channels.JoinChannelAction(channel_guid, 'Remove'))

    def archive_channel(self, channel_guid: str):
        return self(methods.channels.JoinChannelAction(channel_guid, 'Archive'))

    def join_channel_by_link(self, link: str):
        return self(methods.channels.JoinChannelByLink(link))

    def add_channel_members(self, channel_guid: str, member_guids: list):
        return self(methods.channels.AddChannelMembers(channel_guid, member_guids))

    def ban_channel_member(self, channel_guid: str, member_guid: str):
        return self(methods.channels.BanChannelMember(channel_guid, member_guid, 'Set'))

    def unban_channel_member(self, channel_guid: str, member_guid: str):
        return self(methods.channels.BanChannelMember(channel_guid, member_guid, 'Unset'))

    def check_channel_username(self, username: str):
        return self(methods.channels.CheckChannelUsername(username))

    def channel_preview_by_join_link(self, link: str):
        return self(methods.channels.ChannelPreviewByJoinLink(link))

    def get_channel_all_members(self, channel_guid: str, search_text: str = None, start_id: int = None):
        return self(methods.channels.GetChannelAllMembers(channel_guid, search_text, start_id))

    def check_join(self, channel_guid: str, username: str) -> bool:
        result = self.get_channel_all_members(channel_guid, username.replace('@', ''))
        in_chat_members: dict = result['in_chat_members']
        for member in in_chat_members:
            if username in member.values():
                return True
            else:
                continue
        else:
            return False

    def get_channel_admin_members(self, channel_guid: str, start_id: int = None):
        return self(methods.channels.GetChannelAdminMembers(channel_guid, start_id))

    def update_channel_username(self, channel_guid: str, username: str):
        return self(methods.channels.UpdateChannelUsername(channel_guid, username))

    def get_channel_link(self, channel_guid: str):
        return self(methods.channels.GetChannelLink(channel_guid))

    def set_channel_link(self, channel_guid: str):
        return self(methods.channels.SetChannelLink(channel_guid))

    def get_channel_admin_access_list(self, channel_guid: str, member_guid: str):
        return self(methods.channels.GetChannelAdminAccessList(channel_guid, member_guid))

# ---------------- Contacts Methods ----------------

    def delete_contact(self, user_guid: str):
        return self(methods.contacts.DeleteContact(user_guid))

    def add_address_book(self, phone: str, first_name: str, last_name: str = ''):
        return self(methods.contacts.AddAddressBook(phone, first_name, last_name))

    def get_contacts_updates(self, state: int = None):
        return self(methods.contacts.GetContactsUpdates(state))

    def get_contacts(self, start_id: int = None):
        return self(methods.contacts.GetContacts(start_id))

# ---------------- Settings Methods ----------------

    def set_setting(self,
            show_my_last_online: str = None,
            show_my_phone_number: str = None,
            show_my_profile_photo: str = None,
            link_forward_message: str = None,
            can_join_chat_by: str = None
    ):
        updated_parameters = []

        if show_my_last_online:
            updated_parameters.append('show_my_last_online')
        if show_my_phone_number:
            updated_parameters.append('show_my_phone_number')
        if show_my_profile_photo:
            updated_parameters.append('show_my_profile_photo')
        if link_forward_message:
            updated_parameters.append('link_forward_message')
        if can_join_chat_by:
            updated_parameters.append('can_join_chat_by')

        return self(methods.settings.SetSetting(
            updated_parameters,
            show_my_last_online,
            show_my_phone_number,
            show_my_profile_photo,
            link_forward_message,
            can_join_chat_by))

    def add_folder(self,
            include_chat_types: list = None,
            exclude_chat_types: list = None,
            include_object_guids: list = None,
            exclude_object_guids: list = None
    ):
        return self(methods.settings.AddFolder(
            include_chat_types,
            exclude_chat_types,
            include_object_guids,
            exclude_object_guids))

    def get_folders(self, last_state: int):
        return self(methods.settings.GetFolders(last_state))

    def edit_folder(self,
            include_chat_types: list = None,
            exclude_chat_types: list = None,
            include_object_guids: list = None,
            exclude_object_guids: list = None
    ):
        updated_parameters = []

        if include_chat_types:
            updated_parameters.append('include_chat_types')
        if exclude_chat_types:
            updated_parameters.append('exclude_chat_types')
        if include_object_guids:
            updated_parameters.append('include_object_guids')
        if exclude_object_guids:
            updated_parameters.append('exclude_object_guids')

        return self(methods.settings.EditFolder(
            updated_parameters,
            include_chat_types,
            exclude_chat_types,
            include_object_guids,
            exclude_object_guids))

    def delete_folder(self, folder_id: str):
        return self(methods.settings.DeleteFolder(folder_id))

    def update_profile(self, first_name: str = None, last_name: str = None, bio: str = None):
        updated_parameters = []

        if first_name:
            updated_parameters.append('first_name')
        if last_name:
            updated_parameters.append('last_name')
        if bio:
            updated_parameters.append('bio')

        return self(methods.settings.UpdateProfile(updated_parameters, first_name, last_name, bio))

    def update_username(self, username: str):
        return self(methods.settings.UpdateUsername(username))

    def get_two_passcode_status(self):
        return self(methods.settings.GetTwoPasscodeStatus())

    def get_suggested_folders(self):
        return self(methods.settings.GetSuggestedFolders())

    def get_privacy_setting(self):
        return self(methods.settings.GetPrivacySetting())

    def get_blocked_users(self):
        return self(methods.settings.GetBlockedUsers())

    def get_my_sessions(self):
        return self(methods.settings.GetMySessions())

    def terminate_session(self, session_key: str):
        return self(methods.settings.TerminateSession(session_key))

    def setup_two_step_verification(self, password: str, hint: str, recovery_email: str):
        return self(methods.settings.SetupTwoStepVerification(password, hint, recovery_email))

# ---------------- Stickers Methods ----------------

    def get_my_sticker_sets(self):
        return self(methods.stickers.GetMyStickerSets())

    def search_stickers(self, search_text: str = '', start_id: int = None):
        return self(methods.stickers.SearchStickers(search_text, start_id))

    def get_sticker_set_by_ID(self, sticker_set_id: str):
        return self(methods.stickers.GetStickerSetByID(sticker_set_id))

    def action_on_sticker_set(self, sticker_set_id: str, action: str = 'Add'):
        return self(methods.stickers.ActionOnStickerSet(sticker_set_id, action))

    def get_stickers_by_emoji(self, emoji: str, suggest_by: str = 'Add'):
        return self(methods.stickers.GetStickersByEmoji(emoji, suggest_by))

    def get_stickers_by_set_IDs(self, sticker_set_ids: list):
        return self(methods.stickers.GetStickersBySetIDs(sticker_set_ids))

    def get_trend_sticker_sets(self, start_id: int = None):
        return self(methods.stickers.GetTrendStickerSets(start_id))